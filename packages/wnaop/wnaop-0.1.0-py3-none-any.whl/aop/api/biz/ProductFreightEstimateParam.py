# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class ProductFreightEstimateParam(BaseApi):
    """根据商品ID、中国国内收货地址的省市区编码，预估商品的运费。


    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.access_token = None
        self.productFreightQueryParamsNew = None

    def get_api_uri(self):
        return '1/com.alibaba.fenxiao.crossborder/product.freight.estimate'

    def get_required_params(self):
        return ['productFreightQueryParamsNew']

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
