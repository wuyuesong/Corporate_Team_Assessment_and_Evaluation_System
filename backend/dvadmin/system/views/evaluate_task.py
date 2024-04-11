import hashlib
import uuid
import time
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
from dvadmin.system.models import Users, Role, Dept, Department, EvaluateTask, Task, Staff
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
        "evaluate_id",
        "task_weight",
        "evaluated_id",
        "score",
        "grade_complete",
        "grade_date"
    ]
    # search_fields = ["username", "name", "dept__name", "role__name"]
    search_fields = "__all__"
    # 导出
    export_field_label = {
        "evaluate_id":"评价人系统id",
        "task_weight": "任务权重",
        "evaluated_id":"被评价人系统id",
        "score": "分数",
        "grade_complete": "完成情况",
        "grade_date":"评价时间"
    }
    export_serializer_class = ExportEvaluateTaskProfileSerializer
    # 导入
    import_serializer_class = EvaluateTaskProfileImportSerializer

    import_field_dict = {
        "evaluate_id":"评价人系统id",
        "task_weight": "任务权重",
        "evaluated_id":"被评价人系统id",
        "score": "分数",
        "grade_complete": "完成情况",
        "grade_date":"评价时间"
    }

    def evaluate_task_create(self, request: Request):
        task_id = uuid.uuid4()
        task_name = request.data.get("task_name")
        task_describe = request.data.get("task_describe")
        task_start_date = request.data.get("task_start_date")
        task_start_date = datetime.strptime(task_start_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        task_end_date = request.data.get("task_end_date")
        task_end_date = datetime.strptime(task_end_date, '%Y-%m-%dT%H:%M:%S.%fZ')
        task_create_date = datetime.now()
        Task(task_id=task_id, task_name=task_name, task_describe=task_describe, task_start_date=task_start_date, task_end_date=task_end_date, task_create_date=task_create_date, task_type=0).save()
        evaluate = request.data.get("evaluate")
        evaluated = request.data.get("evaluated")
        # time1 = time.time()
        tmp_list =[]
        for evaluate_one in evaluate:
            for evaluated_one in evaluated:
                tmp_list.append(EvaluateTask(task_id=task_id, evaluate_id=evaluate_one["evaluate_id"], task_weight=evaluate_one["task_weight"],evaluated_id=evaluated_one["evaluated_id"]))
        EvaluateTask.objects.bulk_create(tmp_list)
        # time2 = time.time()
        # print("生成任务耗时：", time2 - time1)
        return DetailResponse(data=dict(task_id=task_id), msg="创建成功")

    @action(methods=['POST'], detail=False, permission_classes=[])
    def evaluate_task_info(self, request: Request):
        task_id = request.data.get("task_id")
        staff_id = request.data.get("staff_id")
        evaluated_id_list = list(EvaluateTask.objects.filter(task_id=task_id, evaluate_id=staff_id).values_list('evaluated_id', flat=True).distinct().order_by('evaluated_id'))
        evaluated_queryset = Staff.objects.filter(staff_id__in=evaluated_id_list)
        ret = []
        for evaluated in evaluated_queryset:
            ret.append(dict(evaluated_id=evaluated.staff_id, evaluated_name=evaluated.staff_name, evaluated_rank=evaluated.staff_rank, evaluated_department=evaluated.staff_department))

        return DetailResponse(data=ret, msg="查询成功")
    
    @action(methods=['POST'], detail=False, permission_classes=[])
    def submit_evaluate_task(self, request: Request):
        evaluate_id = request.data.get("evaluate_id")
        task_id = request.data.get("task_id")
        scores = request.data.get("scores")
        
        for score in scores:
            evaluated_id = score["evaluated_id"]
            EvaluateTask.objects.filter(evaluate_id=evaluate_id, task_id=task_id, evaluated_id=evaluated_id).update(score=score["score"],grade_complete=1,grade_date=datetime.now())

        return DetailResponse(data=[], msg="提交成功")


    def evaluate_task_delete_all(self, request: Request):
        EvaluateTask_all = EvaluateTask.objects.all()
        EvaluateTask_all.delete()
        return DetailResponse(data=[], msg="删除成功")
    

    @action(methods=['POST'], detail=False, permission_classes=[])
    def task_info(self, request: Request):
        task_id = request.data.get("task_id")
        task = Task.objects.get(task_id=task_id)

        all_evaluate = list(EvaluateTask.objects.filter(task_id=task_id).values_list('evaluate_id', flat=True).distinct().order_by('evaluate_id'))
        undo_staff_id_list = list(EvaluateTask.objects.filter(task_id=task_id, grade_complete=0).values_list('evaluate_id', flat=True).distinct().order_by('evaluate_id'))
        undo_staff_info = Staff.objects.filter(staff_id__in=undo_staff_id_list)

        ret = {"task_id":task.task_id,
                "task_name":task.task_name,
                "task_describe":task.task_describe,
                "task_start_date":task.task_start_date,
                "task_end_date":task.task_end_date,
                "task_create_date":task.task_create_date,
                "staff_count":len(all_evaluate),}
        undo_staff = []
        for staff in undo_staff_info:
            undo_staff.append({
                "staff_name":staff.staff_name,
                "staff_firm_id":staff.staff_id,
                "staff_department":staff.staff_department
            })

        ret["undo_staff"] = undo_staff

        return DetailResponse(data=ret, msg="获取成功")     


