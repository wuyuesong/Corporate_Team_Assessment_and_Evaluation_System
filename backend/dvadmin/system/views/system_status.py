# -*- coding: utf-8 -*-

"""
@author: 吴岳松
@Created on: 2024/5/24
@Remark: 系统状态
"""

import django_filters
from django.db.models import Q
from django_filters.rest_framework import BooleanFilter
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.decorators import action

from application import dispatch
from dvadmin.system.models import SystemConfig, SystemStatus
from dvadmin.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
from dvadmin.utils.models import get_all_models_objects
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.validator import CustomValidationError
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.json_response import ErrorResponse, DetailResponse, SuccessResponse



class SystemStatusViewSet(CustomModelViewSet):
    """
    系统状态接口
    """
    queryset = SystemConfig.objects.order_by('sort', 'create_datetime')

    @action(methods=['GET'], detail=False, permission_classes=[])
    def get_status(self, request: Request):
        system_status_all = SystemStatus.objects.all()

        ret = []
        for system_status in system_status_all:
            ret.append(dict(key=system_status.key, value=system_status.value))
        
        return DetailResponse(data=ret, msg="获取成功")
    

    @action(methods=['POST'], detail=False, permission_classes=[])
    def set_last_email_time(self, request: Request):
        last_email_time = request.data.get("last_email_time")
        last_email_time_status = SystemStatus.objects.get(key="last_email_time")
        last_email_time_status.last_email_time = last_email_time

        return DetailResponse(data=[], msg="设置成功")

