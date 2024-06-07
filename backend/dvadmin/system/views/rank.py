"""
@author: wuyuesong
@Remark: 职级管理
"""

import hashlib
import string

from django.contrib.auth.hashers import make_password, check_password
from django_restql.fields import DynamicSerializerMethodField
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from django.db import connection
from django.db.models import Q
from application import dispatch
from dvadmin.system.models import Users, Role, Dept, Rank, Department
from dvadmin.system.views.role import RoleSerializer
from dvadmin.utils.json_response import ErrorResponse, DetailResponse, SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.validator import CustomUniqueValidator
from dvadmin.utils.viewset import CustomModelViewSet



class RankSerializer(CustomModelSerializer):
    """
    用户管理-序列化器
    """
    class Meta:
        model = Rank
        fields = "__all__"



class RankCreateSerializer(CustomModelSerializer):
    """
    用户新增-序列化器
    """


    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()
        return data

    class Meta:
        model = Rank
        fields = "__all__"



class RankUpdateSerializer(CustomModelSerializer):
    """
    用户修改-序列化器
    """


    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()

        return data

    class Meta:
        model = Rank
        fields = "__all__"



class RankInfoUpdateSerializer(CustomModelSerializer):
    """
    用户修改-序列化器
    """
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Rank
        fields = "__all__"


class ExportRankProfileSerializer(CustomModelSerializer):
    """
    用户导出 序列化器
    """
    class Meta:
        model = Rank
        fields = "__all__"



class RankProfileImportSerializer(CustomModelSerializer):
    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()
        return data

    class Meta:
        model = Rank
        fields = "__all__"


class RankViewSet(CustomModelViewSet):
    """
    用户接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = Rank.objects.all()
    serializer_class = RankSerializer
    create_serializer_class = RankCreateSerializer
    update_serializer_class = RankUpdateSerializer
    filter_fields = [
        "normal_rank",
        "staff_rank",
        "normal_department",
        "staff_department"
    ]
    search_fields = "__all__"
    # 导出
    export_field_label = {
        "normal_rank": "用户标准化职级",
        "staff_rank": "职位等级",
        "normal_department": "用户标准化部门",
        "staff_department": "用户部门"
    }
    export_serializer_class = ExportRankProfileSerializer
    # 导入
    import_serializer_class = RankProfileImportSerializer

    import_field_dict = {
        "normal_rank": "用户标准化职级",
        "staff_rank": "职位等级",
        "normal_department": "用户标准化部门",
        "staff_department": "用户部门"
    }

    # 删除所有职级
    def Rank_delete_all(self, request: Request):
        Rank_all = Rank.objects.all()
        Rank_all.delete()
        return DetailResponse(data=[], msg="删除成功")
    
    # 获取所有职级
    def unique_rank_list(self, request: Request):
        unique_rank = list(Rank.objects.order_by('staff_rank').values_list('staff_rank', flat=True).distinct().order_by('staff_rank'))
        dist_unique_rank = [dict(name=rank,id=value) for value,rank in enumerate(unique_rank, start=1)]
        return DetailResponse(data=dist_unique_rank, msg="获取成功")
    

    # 以树形结构的方式获取职级
    def tree_rank_list(self, request: Request):
        chinese_numerals = {
            0: '零', 1: '一', 2: '二', 3: '三', 4: '四',
            5: '五', 6: '六', 7: '七', 8: '八', 9: '九'
        }
        rank_list = Rank.objects.all()
        department_list = Department.objects.all()
        ret = []
        for letter in string.ascii_lowercase:
            for department in department_list:
                if (letter in department.normal_department) or (letter.upper() in department.normal_department):
                    ret.append(dict())
                    offset = ord(letter) - ord('a')
                    ret[offset] = dict(id=f"a-{offset + 1}",value=f"{chinese_numerals[offset + 1]}级部门", children=[])
                    break
        
        for department in department_list:
            if department.normal_department[0].isupper():
                offset = ord(department.normal_department[0]) - ord('A')
            elif department.normal_department[0].islower():
                offset = ord(department.normal_department[0]) - ord('a')

            department_id = department.normal_department[1:3].lstrip('0')
            tmp_dict = dict(id=f"b-{department_id}",value=f"{department.staff_department}", children=[])
            
            current_department_rank = Rank.objects.filter(staff_department=department.staff_department)
            for id,rank in enumerate(current_department_rank, start=1):
                tmp_dict['children'].append(dict(id=f"c-{department.staff_department}-{rank.staff_rank}",value=f"{rank.staff_rank}", children=[]) )
            
            ret[offset]['children'].append(tmp_dict)
            
        return DetailResponse(data=ret, msg="获取成功")
    

    @action(methods=['GET'], detail=False, permission_classes=[])
    def rank_delete_all(self, request: Request):
        
        rank_all = Rank.objects.all()
        rank_all.delete()
        
        return DetailResponse(data=[], msg="删除成功")
        
                
                
            
        
            



