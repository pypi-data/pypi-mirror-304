# -*- coding: utf-8 -*-
from aop.api.base import BaseApi

class CategoryTranslationGetByIdParam(BaseApi):
    """多语言类目查询接口。根据当前语种和类目ID查询对应语种的类目详情，包含当前类目的下级类目列表数据。


    """

    def __init__(self, domain=None):
        BaseApi.__init__(self, domain)
        self.access_token = None
        self.outMemberId = None
        self.language = None
        self.categoryId = None
        self.parentCateId = None

    def get_api_uri(self):
        return '1/com.alibaba.fenxiao.crossborder/category.translation.getById'

    def get_required_params(self):
        return ['outMemberId', 'language', 'categoryId', 'parentCateId']

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
