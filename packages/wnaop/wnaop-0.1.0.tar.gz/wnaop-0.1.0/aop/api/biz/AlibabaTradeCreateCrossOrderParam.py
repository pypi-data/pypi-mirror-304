# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class AlibabaTradeCreateCrossOrderParam(BaseApi):
    """跨境专用订单创建。创建订单最多允许100个SKU，且必须为同一个供应商的商品。超过50个SKU或者一些特殊情况会一次创建多个个订单并返回多个订单号。
支持大市场及分销两个场景。根据当前授权用户,区分主子账号下单

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.alibaba.trade&n=alibaba.trade.createCrossOrder&v=1&cat=order_category

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.access_token = None
        self.flow = None
        self.message = None
        self.isvBizType = None
        self.addressParam = None
        self.cargoParamList = None
        self.invoiceParam = None
        self.tradeType = None
        self.shopPromotionId = None
        self.anonymousBuyer = None
        self.fenxiaoChannel = None
        self.inventoryMode = None
        self.outOrderId = None
        self.pickupService = None
        self.warehouseCode = None
        self.preSelectPayChannel = None
        self.smallProcurement = None
        self.useRedEnvelope = None
        self.dropshipping = None
        self.addedService = None

    def get_api_uri(self):
        return '1/com.alibaba.trade/alibaba.trade.createCrossOrder'

    def get_required_params(self):
        return ['flow', 'message', 'isvBizType', 'addressParam', 'cargoParamList', 'invoiceParam', 'tradeType', 'shopPromotionId', 'anonymousBuyer', 'fenxiaoChannel', 'inventoryMode', 'outOrderId', 'pickupService', 'warehouseCode', 'preSelectPayChannel', 'smallProcurement', 'useRedEnvelope', 'dropshipping', 'addedService']

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
