# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class AlibabaCategoryAttributeGetParam(BaseApi):
    """根据叶子类目ID获取类目属性

    References
    ----------
    https://open.1688.com/api/api.htm?ns=com.alibaba.product&n=alibaba.category.attribute.get&v=1&cat=aop.category

    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.access_token = None
        self.categoryID = None
        self.webSite = None
        self.scene = None

    def get_api_uri(self):
        return '1/com.alibaba.product/alibaba.category.attribute.get'

    def get_required_params(self):
        return ['categoryID', 'webSite', 'scene']

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
