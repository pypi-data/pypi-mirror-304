# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class ConsignmentCoInventoryParam(BaseApi):
    """仓库商品库存更新


    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.bizSkuId = None
        self.sourceItemId = None
        self.outboundQuantity = None
        self.bizId = None

    def get_api_uri(self):
        return '1/com.alibaba.fenxiao.crossborder/consignment.co.inventory'

    def get_required_params(self):
        return ['bizSkuId', 'sourceItemId', 'outboundQuantity', 'bizId']

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
