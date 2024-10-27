# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class ProductKjdistributeAddRelationParam(BaseApi):
    """增加跨境关注商品


    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.offerId = None

    def get_api_uri(self):
        return '1/com.alibaba.fenxiao.crossborder/product.kjdistribute.addRelation'

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
