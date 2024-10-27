# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class ProductDistributeGetDistributeInfoParam(BaseApi):
    """用于铺货场景下，获取铺货需要的卖点信息


    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.offerId = None

    def get_api_uri(self):
        return '1/com.alibaba.fenxiao.crossborder/product.distribute.getDistributeInfo'

    def get_required_params(self):
        return ['offerId']

    def get_multipart_params(self):
        return []

    def need_sign(self):
        return True

    def need_timestamp(self):
        return False

    def need_auth(self):
        return False

    def need_https(self):
        return False

    def is_inner_api(self):
        return False
