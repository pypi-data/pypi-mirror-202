import logging
import random
from datetime import datetime

import pytz
import requests
import time

from django.core.paginator import Paginator
from django.db.models import F
from django.forms import model_to_dict
from django.utils import timezone
from pathlib import Path
from main.settings import BASE_DIR
from xj_common.utils.custom_tool import format_list_handle, format_params_handle
from xj_user.models import Platform
from xj_user.services.user_platform_service import UserPlatformService
from ..utils.j_config import JConfig
from ..utils.j_dict import JDict
from xj_finance.services.finance_service import FinanceService
from xj_finance.services.finance_transact_service import FinanceTransactService
from xj_enroll.service.enroll_services import EnrollServices
from xj_thread.services.thread_item_service import ThreadItemService
from xj_user.services.user_service import UserService
from xj_payment.models import PaymentPayment, PaymentStatus
from xj_user.services.user_sso_serve_service import UserSsoServeService
from ..services.payment_wechat_service import PaymentWechatService

module_root = str(Path(__file__).resolve().parent)
# 配置之对象
main_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))
module_config_dict = JDict(JConfig.get_section(path=str(BASE_DIR) + "/config.ini", section="xj_payment"))

sub_appid = main_config_dict.wechat_merchant_app_id or module_config_dict.wechat_merchant_app_id or ""
# 商户名称
merchant_name = main_config_dict.merchant_name or module_config_dict.merchant_name or ""


class InvalidPage(Exception):
    pass


class PageNotAnInteger(InvalidPage):
    pass


class EmptyPage(InvalidPage):
    pass


class PaymentService:
    @staticmethod
    def get(params):
        limit = params.pop('limit', 20)
        page = params.pop('page', 20)
        print(params.get("create_time_start", None))
        list_obj = PaymentPayment.objects.filter(**params).order_by('-id')
        if params.get("create_time_start", None) and params.get("create_time_end", None):
            list_obj = list_obj.filter(
                create_time__range=(params['create_time_start'], params['create_time_end']))

        list_obj = list_obj.annotate(payment_status=F("payment_status__payment_status"),
                                     payment_code=F("payment_status__payment_code"))

        if params.get("payment_status", None):
            list_obj = list_obj.filter(payment_status__payment_status=params.get("payment_status", None), )

        list_obj = list_obj.extra(select={
            'user_full_name': 'SELECT full_name FROM user_base_info WHERE user_base_info.id = payment_payment.user_id'}
        )
        list_obj = list_obj.extra(select={
            'title': 'SELECT thread.title FROM enroll_enroll left join  thread on enroll_enroll.thread_id=thread.id WHERE enroll_enroll.id = payment_payment.enroll_id'}
        )
        count = list_obj.count()
        list_obj = list_obj.values(
            "id",
            "transact_no",
            "order_no",
            "transact_id",
            "enroll_id",
            "order_id",
            "user_id",
            "subject",
            "total_amount",
            "buyer_pay_amount",
            "point_amount",
            "invoice_amount",
            "price_off_amount",
            "pay_mode",
            "order_status_id",
            "payment_status_id",
            "nonce_str",
            "order_time",
            "create_time",
            "modify_time",
            "payment_time",
            "refunt_time",
            "close_time",
            "voucher_detail",
            "snapshot",
            "more",
            "user_full_name",
            "title",
            "payment_status"

        ).annotate(payment_status=F('payment_status__payment_status'), )
        res_set = Paginator(list_obj, limit).get_page(page)
        page_list = []
        if res_set:
            page_list = list(res_set.object_list)
        for v in page_list:
            v['total_amount'] = float(v['total_amount']) / 100 if v['total_amount'] is not None else 0
            v['point_amount'] = float(v['point_amount']) / 100 if v['point_amount'] is not None else 0
            v['buyer_pay_amount'] = float(v['buyer_pay_amount']) / 100 if v['buyer_pay_amount'] is not None else 0
            v['invoice_amount'] = float(v['invoice_amount']) / 100 if v['invoice_amount'] is not None else 0
            v['price_off_amount'] = float(v['price_off_amount']) / 100 if v['price_off_amount'] is not None else 0

        return {'count': count, 'page': page, 'limit': limit, "list": page_list}, None

    @staticmethod
    def list(params, filter_fields=None, need_pagination=True):
        size = params.pop('limit', 10)
        page = params.pop('page', 1)
        print(params)
        filter_fields_list = filter_fields.split(";") if filter_fields else []
        params = format_params_handle(
            param_dict=params,
            filter_filed_list=[
                "id", "transact_no", "order_no", "transact_id", "enroll_id", "order_id",
                "user_id", "subject", "total_amount", "buyer_pay_amount", "point_amount",
                "invoice_amount", "price_off_amount", "pay_mode", "order_status_id", "create_time",
                "payment_status_id", "nonce_str", "order_time", "modify_time", "payment_time", "refunt_time",
                "close_time",
                "create_time_start", "create_time_end"
            ],
            split_list=["user_id_list", "id_list", "enroll_id_list", "thread_id_list"],
            alias_dict={
                "modify_time_start": "modify_time__gte", "modify_time_end": "modify_time__lte",
                "create_time_start": "create_time__gte", "create_time_end": "create_time__lte",
                "enroll_category_value": "category__value",
                "thread_id_list": "thread_id__in", "enroll_id_list": "enroll_id__in", "id_list": "id__in",
            },
        )
        enroll_obj = PaymentPayment.objects.filter(**params).order_by("-id").values(*filter_fields_list)
        print(enroll_obj)
        if not need_pagination:
            return list(enroll_obj), None

        # 分页展示
        paginator = Paginator(enroll_obj, size)
        try:
            enroll_obj = paginator.page(page)
        except EmptyPage:
            enroll_obj = paginator.page(paginator.num_pages)
        except Exception as e:
            return None, f'{str(e)}'
        return {'total': paginator.count, "page": page, "size": size, 'list': list(enroll_obj.object_list)}, None

    # 支付总接口
    @staticmethod
    def pay(params):
        data = params
        out_trade_no = timezone.now().strftime('%Y%m%d%H%M%S') + ''.join(
            map(str, random.sample(range(0, 9), 4)))  # 随机生成订单号
        params['out_trade_no'] = out_trade_no
        if params['enroll_id']:
            enroll_data, err_txt = EnrollServices.enroll_detail(params['enroll_id'])  # 判断是否是报名订单
            if err_txt:
                return "报名记录不存在"
            data['enroll_id'] = enroll_data['id']
            data['user_id'] = enroll_data['user_id']
            data['total_fee'] = float(enroll_data['unpaid_amount']) * 100  # 元转分
        # 单点登录信息
        sso_data, err = UserSsoServeService.user_sso_to_user(data['user_id'], sub_appid)
        if err:
            return "单点登录记录不存在"
        sso_data = model_to_dict(sso_data)
        data['openid'] = sso_data['sso_unicode']
        tz = pytz.timezone('Asia/Shanghai')
        # 返回datetime格式的时间
        now_time = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
        payment_status_set = PaymentStatus.objects.filter(payment_status="未支付").first()
        payment_data = {
            "order_no": out_trade_no,
            "enroll_id": data['enroll_id'],
            "user_id": data['user_id'],
            "total_amount": int(data['total_fee']),
            "create_time": now,
            "payment_status_id": payment_status_set.id
        }

        platform_set, err = UserPlatformService.payment_get_platform_info(params['platform_id'])
        if err:
            data['platform'] = merchant_name
        else:
            data['platform'] = platform_set['platform_name']

        data['currency'] = 'CNY'

        if params.get("total_amount", 0):
            data['total_fee'] = float(params.get("total_amount", 0)) * 100  # 元转分

        if data['total_fee'] < 1:
            return "支付金额不能小于一分钱"

        # 支付方式检查
        if params['payment_method'] == "applets":  # 微信小程序支付

            payment = PaymentWechatService.payment_applets_pay(data)

        elif params['payment_method'] == "appletsv3":  # 微信小程序支付v3
            payment = PaymentWechatService.payment_applets_pay_v3(data)

        elif params['payment_method'] == "balance":  # 余额支付
            payment = PaymentWechatService.payment_balance_pay(data)
        else:
            payment = "支付方式不存在"

        PaymentPayment.objects.create(**payment_data)

        return payment

    # 退款总接口
    @staticmethod
    def refund(params):
        data = params
        data['transaction_id'] = params['transaction_id']  # 支付单号
        data['refund_fee'] = float(params['refund_amount']) * 100  # 元转分
        data['out_trade_no'] = timezone.now().strftime('%Y%m%d%H%M%S') + ''.join(
            map(str, random.sample(range(0, 9), 4)))
        # 支付方式检查
        if params['payment_method'] == "WECHAT":  # 微信退款
            payment = PaymentWechatService.payment_refund(data)
        else:
            payment = "退款方式不存在"

        return payment

        # 支付总接口

    @staticmethod
    def pay_v2(params):
        data = params
        payment_method = params.get("payment_method", None)
        payment_method_list = ["applets", "appletsv3", "balance"]
        if not PaymentService.find(payment_method_list, payment_method):
            return None, "支付方式不存在"

        out_trade_no = timezone.now().strftime('%Y%m%d%H%M%S') + ''.join(
            map(str, random.sample(range(0, 9), 4)))  # 随机生成订单号
        params['out_trade_no'] = out_trade_no
        if params['enroll_id']:
            enroll_data, err_txt = EnrollServices.enroll_detail(params['enroll_id'])  # 判断是否是报名订单
            if err_txt:
                return None, "报名记录不存在"
            data['enroll_id'] = enroll_data['id']
            data['user_id'] = enroll_data['user_id']
            data['total_fee'] = float(enroll_data['unpaid_amount']) * 100  # 元转分
        # 单点登录信息
        sso_data, err = UserSsoServeService.user_sso_to_user(data['user_id'], sub_appid)
        if err:
            return None, "单点登录记录不存在"
        sso_data = model_to_dict(sso_data)
        data['openid'] = sso_data['sso_unicode']
        tz = pytz.timezone('Asia/Shanghai')
        # 返回datetime格式的时间
        now_time = timezone.now().astimezone(tz=tz).strftime("%Y-%m-%d %H:%M:%S")
        now = datetime.strptime(now_time, '%Y-%m-%d %H:%M:%S')
        payment_status_set = PaymentStatus.objects.filter(payment_status="未支付").first()
        payment_data = {
            "order_no": out_trade_no,
            "enroll_id": data['enroll_id'],
            "user_id": data['user_id'],
            "total_amount": int(data['total_fee']),
            "create_time": now,
            "payment_status_id": payment_status_set.id
        }

        platform_set, err = UserPlatformService.payment_get_platform_info(params['platform_id'])
        if err:
            data['platform'] = merchant_name
        else:
            data['platform'] = platform_set['platform_name']

        data['currency'] = 'CNY'

        if params.get("total_amount", 0):
            data['total_fee'] = float(params.get("total_amount", 0)) * 100  # 元转分

        if data['total_fee'] < 1:
            return None, "支付金额不能小于一分钱"

        try:
            PaymentPayment.objects.create(**payment_data)

            # 支付方式检查
            if params['payment_method'] == "applets":  # 微信小程序支付

                payment = PaymentWechatService.payment_applets_pay(data)

            elif params['payment_method'] == "appletsv3":  # 微信小程序支付v3
                payment = PaymentWechatService.payment_applets_pay_v3(data)

            elif params['payment_method'] == "balance":  # 余额支付
                payment = PaymentWechatService.payment_balance_pay(data)
        except Exception as e:
            return None, str(e)

        return payment, None

    @staticmethod
    def find(list, keyword):
        try:
            list.index(keyword)
            return True
        except ValueError:
            return False
