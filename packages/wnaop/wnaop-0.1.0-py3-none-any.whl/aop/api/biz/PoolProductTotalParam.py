# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class PoolProductTotalParam(BaseApi):
    """查询商品池中商品总数


    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.appKey = None
        self.palletId = None
        self.categoryId = None

    def get_api_uri(self):
        return '1/com.alibaba.fenxiao.crossborder/pool.product.total'

    def get_required_params(self):
        return ['appKey', 'palletId', 'categoryId']

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
