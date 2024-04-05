import hashlib
import uuid
from datetime import datetime

from django.contrib.auth.hashers import make_password, check_password
from django_restql.fields import DynamicSerializerMethodField
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from django.db import connection
from django.db.models import Q
from application import dispatch
from dvadmin.system.models import Users, Role, Dept, Department, EvaluateTask, Task
from dvadmin.system.views.role import RoleSerializer
from dvadmin.utils.json_response import ErrorResponse, DetailResponse, SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.validator import CustomUniqueValidator
from dvadmin.utils.viewset import CustomModelViewSet



class EvaluateTaskSerializer(CustomModelSerializer):
    """
    用户管理-序列化器
    """

    class Meta:
        model = EvaluateTask
        fields = "__all__"


class EvaluateTaskCreateSerializer(CustomModelSerializer):
    """
    用户新增-序列化器
    """

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()
        return data

    class Meta:
        model = EvaluateTask
        fields = "__all__"


class EvaluateTaskUpdateSerializer(CustomModelSerializer):
    """
    用户修改-序列化器
    """
    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()
        return data

    class Meta:
        model = EvaluateTask
        fields = "__all__"
        

class EvaluateTaskInfoUpdateSerializer(CustomModelSerializer):
    """
    用户修改-序列化器
    """

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = EvaluateTask
        fields = "__all__"


class ExportEvaluateTaskProfileSerializer(CustomModelSerializer):
    """
    用户导出 序列化器
    """

    class Meta:
        model = EvaluateTask
        fields = "__all__"


class EvaluateTaskProfileImportSerializer(CustomModelSerializer):

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()
        return data

    class Meta:
        model = EvaluateTask
        fields = "__all__"


class EvaluateTaskViewSet(CustomModelViewSet):
    """
    用户接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = EvaluateTask.objects.all()
    serializer_class = EvaluateTaskSerializer
    create_serializer_class = EvaluateTaskCreateSerializer
    update_serializer_class = EvaluateTaskUpdateSerializer
    # filter_fields = ["name", "username", "gender", "is_active", "dept", "user_type"]
    filter_fields = [
        "evaluate_name",
        "evaluate_describe",
        "task_start_date",
        "task_end_date", 
        "task_create_date",
        "evaluate_id",
        "task_weight",
        "evaluated_id",
        "score",
        "grade_complete",
        "task_create_date",
        "grade_date"
    ]
    # search_fields = ["username", "name", "dept__name", "role__name"]
    search_fields = "__all__"
    # 导出
    export_field_label = {
        "evaluate_name":"评价任务名称",
        "evaluate_describe":"评价任务描述",
        "task_start_date":"任务开始时间",
        "task_end_date":"任务结束时间", 
        "task_create_date":"任务创建时间",
        "evaluate_id":"评价人系统id",
        "task_weight": "任务权重",
        "evaluated_id":"被评价人系统id",
        "score": "分数",
        "grade_complete": "完成情况",
        "task_create_date":"任务创建时间",
        "grade_date":"评价时间"
    }
    export_serializer_class = ExportEvaluateTaskProfileSerializer
    # 导入
    import_serializer_class = EvaluateTaskProfileImportSerializer

    import_field_dict = {
        "evaluate_name":"评价任务名称",
        "evaluate_describe":"评价任务描述",
        "task_start_date":"任务开始时间",
        "task_end_date":"任务结束时间", 
        "task_create_date":"任务创建时间",
        "evaluate_id":"评价人系统id",
        "task_weight": "任务权重",
        "evaluated_id":"被评价人系统id",
        "score": "分数",
        "grade_complete": "完成情况",
        "task_create_date":"任务创建时间",
        "grade_date":"评价时间"
    }

    def evaluate_task_create(self, request: Request):
        task_id = uuid.uuid4()
        task_name = request.data.get("task_name")
        task_describe = request.data.get("task_describe")
        task_start_date = request.data.get("task_start_date")
        task_end_date = request.data.get("task_end_date")
        task_create_date = datetime.now()
        Task(task_id=task_id, task_name=task_name, task_describe=task_describe, task_start_date=task_start_date, task_end_date=task_end_date, task_create_date=task_create_date)
        evaluate = request.data.get("evaluate")
        evaluated = request.data.get("evaluated")
        for evaluate_one in evaluate:
            for evaluated_one in evaluated:
                EvaluateTask(task_id=task_id, evaluate_id=evaluate_one["evaluate_id"], task_weight=evaluate_one["task_weight"],evaluated_id=evaluated_one["evaluated_id"]).save()
        return DetailResponse(data=dict(task_id=task_id), msg="创建成功")

    
    def evaluate_task_delete_all(self, request: Request):
        EvaluateTask_all = EvaluateTask.objects.all()
        EvaluateTask_all.delete()
        return DetailResponse(data=[], msg="删除成功")


