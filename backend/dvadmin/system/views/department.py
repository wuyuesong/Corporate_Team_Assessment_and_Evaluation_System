"""
@author: wuyuesong
@Remark: 部门管理
"""

import hashlib

from django.contrib.auth.hashers import make_password, check_password
from django_restql.fields import DynamicSerializerMethodField
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from django.db import connection
from django.db.models import Q
from application import dispatch
from dvadmin.system.models import Users, Role, Dept, Department
from dvadmin.system.views.role import RoleSerializer
from dvadmin.utils.json_response import ErrorResponse, DetailResponse, SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.validator import CustomUniqueValidator
from dvadmin.utils.viewset import CustomModelViewSet



class DepartmentSerializer(CustomModelSerializer):
    """
    用户管理-序列化器
    """
    # dept_name = serializers.CharField(source='dept.name', read_only=True)
    # role_info = DynamicSerializerMethodField()
    # dept_name_all = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = "__all__"


class DepartmentCreateSerializer(CustomModelSerializer):
    """
    用户新增-序列化器
    """

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()
        return data

    class Meta:
        model = Department
        fields = "__all__"


class DepartmentUpdateSerializer(CustomModelSerializer):
    """
    用户修改-序列化器
    """

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()
        return data

    class Meta:
        model = Department
        fields = "__all__"


class DepartmentInfoUpdateSerializer(CustomModelSerializer):
    """
    用户修改-序列化器
    """

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Department
        fields = "__all__"


class ExportDepartmentProfileSerializer(CustomModelSerializer):
    """
    用户导出 序列化器
    """
    class Meta:
        model = Department
        fields = "__all__"

class DepartmentProfileImportSerializer(CustomModelSerializer):

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()
        return data

    class Meta:
        model = Department
        fields = "__all__"


class DepartmentViewSet(CustomModelViewSet):
    """
    用户接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    create_serializer_class = DepartmentCreateSerializer
    update_serializer_class = DepartmentUpdateSerializer
    # filter_fields = ["name", "username", "gender", "is_active", "dept", "user_type"]
    filter_fields = [
         "normal_rank",
        "staff_rank",
        # "staff_department",
        # "normal_department"
    ]
    # search_fields = ["username", "name", "dept__name", "role__name"]
    search_fields = "__all__"
    # 导出
    export_field_label = {
        "staff_department": "部门名称",
        "normal_department": "标准化部门"
    }
    export_serializer_class = ExportDepartmentProfileSerializer
    # 导入
    import_serializer_class = DepartmentProfileImportSerializer
    import_field_dict = {
        "staff_department": "部门名称",
        "normal_department": "标准化部门"
    }

    def Department_delete_all(self, request: Request):
        Department_all = Department.objects.all()
        Department_all.delete()
        return DetailResponse(data=[], msg="删除成功")
    

    @action(methods=['GET'], detail=False, permission_classes=[])
    def department_delete_all(self, request: Request):
        
        rank_all = Department.objects.all()
        rank_all.delete()
        
        return DetailResponse(data=[], msg="删除成功")


