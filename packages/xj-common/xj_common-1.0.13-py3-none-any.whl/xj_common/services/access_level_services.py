# encoding: utf-8
"""
@project: djangoModel->access_level_services
@author: 孙楷炎
@Email: sky4834@163.com
@synopsis: 访问级别服务
@created_time: 2023/4/11 20:56
"""
from ..models import AccessLevel


class AccessLevelService():
    @staticmethod
    def access_level_list():
        all_access_level = AccessLevel.objects.all().values().to_json()
        return all_access_level, None
