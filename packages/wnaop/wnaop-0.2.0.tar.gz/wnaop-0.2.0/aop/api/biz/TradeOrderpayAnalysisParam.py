# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class TradeOrderpayAnalysisParam(BaseApi):
    """交易订单支付咨询接口，用于分析订单使用什么支付方式等。


    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.access_token = None
        self.orderIds = None
        self.payChannel = None

    def get_api_uri(self):
        return '1/com.alibaba.trade/trade.orderpay.analysis'

    def get_required_params(self):
        return ['orderIds', 'payChannel']

    def get_multipart_params(self):
        return []

    def need_sign(self):
        return True

    def need_timestamp(self):
        return False

    def need_auth(self):
        return True

    def need_https(self):
        return False

    def is_inner_api(self):
        return False
