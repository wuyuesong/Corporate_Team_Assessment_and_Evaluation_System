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
from dvadmin.system.models import Users, Role, Dept, Department, Task, EvaluateTask, WeightTask
from dvadmin.system.views.role import RoleSerializer
from dvadmin.utils.json_response import ErrorResponse, DetailResponse, SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.validator import CustomUniqueValidator
from dvadmin.utils.viewset import CustomModelViewSet


class TaskSerializer(CustomModelSerializer):
    """
    用户管理-序列化器
    """

    class Meta:
        model = Task
        fields = "__all__"


class TaskCreateSerializer(CustomModelSerializer):
    """
    用户新增-序列化器
    """

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()
        return data

    class Meta:
        model = Task
        fields = "__all__"


class TaskUpdateSerializer(CustomModelSerializer):
    """
    用户修改-序列化器
    """
    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()
        return data

    class Meta:
        model = Task
        fields = "__all__"
        

class TaskInfoUpdateSerializer(CustomModelSerializer):
    """
    用户修改-序列化器
    """

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Task
        fields = "__all__"


class ExportTaskProfileSerializer(CustomModelSerializer):
    """
    用户导出 序列化器
    """

    class Meta:
        model = Task
        fields = "__all__"


class TaskProfileImportSerializer(CustomModelSerializer):

    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()
        return data

    class Meta:
        model = Task
        fields = "__all__"


class TaskViewSet(CustomModelViewSet):
    """
    用户接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    create_serializer_class = TaskCreateSerializer
    update_serializer_class = TaskUpdateSerializer
    # filter_fields = ["name", "username", "gender", "is_active", "dept", "user_type"]
    filter_fields = [
        "task_id",
        "task_name",
        "task_describe",
        "task_start_date",
        "task_end_date", 
        "task_create_date",
    ]
    # search_fields = ["username", "name", "dept__name", "role__name"]
    search_fields = "__all__"
    # 导出
    export_field_label = {
        "task_id": "任务id",
        "task_name":"评价任务名称",
        "task_describe":"评价任务描述",
        "task_start_date":"任务开始时间",
        "task_end_date":"任务结束时间", 
        "task_create_date":"任务创建时间",
    }
    export_serializer_class = ExportTaskProfileSerializer
    # 导入
    import_serializer_class = TaskProfileImportSerializer

    import_field_dict = {
        "task_id": "任务id",
        "task_name":"评价任务名称",
        "task_describe":"评价任务描述",
        "task_start_date":"任务开始时间",
        "task_end_date":"任务结束时间", 
        "task_create_date":"任务创建时间",
    }
    
    # 删除所有任务
    def task_delete_all(self, request: Request):
        Task_all = Task.objects.all()
        Task_all.delete()
        return DetailResponse(data=[], msg="删除成功")
    

    # 获取登录账号所有任务列表
    @action(methods=['POST'], detail=False, permission_classes=[])
    def task_list(self, request: Request):
        staff_id = request.data.get("staff_id")
        user = request.user
        print(user.staff_id)
        cur_evaluate_task_id = list(EvaluateTask.objects.filter(evaluate_id=staff_id).values_list('task_id', flat=True).distinct().order_by('task_id'))
        cur_weight_task_id = list(WeightTask.objects.filter(staff_id=staff_id).values_list('task_id', flat=True).distinct().order_by('task_id'))

        task_id_list = cur_evaluate_task_id + cur_weight_task_id
        task_info = Task.objects.filter(task_id__in=task_id_list)

        ret=[]
        for task in task_info:
            if task.task_type == 0:
                complete_status = EvaluateTask.objects.filter(task_id=task.task_id, evaluate_id=staff_id).first().grade_complete
                ret.append({
                    "task_id":task.task_id,
                    "task_name":task.task_name,
                    "task_describe":task.task_describe,
                    "task_start_date":task.task_start_date,
                    "task_end_date":task.task_end_date,
                    "task_create_date":task.task_create_date,
                    "task_type":task.task_type,
                    "complete_status":complete_status
                })
            elif task.task_type == 1:
                complete_status = WeightTask.objects.filter(task_id=task.task_id, staff_id=staff_id).first().weight_complete
                ret.append({
                    "task_id":task.task_id,
                    "task_name":task.task_name,
                    "task_describe":task.task_describe,
                    "task_create_date":task.task_create_date,
                    "task_type":task.task_type,
                    "complete_status":complete_status
                })

        return DetailResponse(data=ret, msg="获取成功")        
    
    # 获取所有任务的列表，与前面不同，这里是所有人的任务
    @action(methods=['GET'], detail=False, permission_classes=[])
    def task_list_all(self, request: Request):
        Task_all = Task.objects.all()
        ret=[]
        for task in Task_all:
            ret.append({
                "task_id":task.task_id,
                "task_name":task.task_name,
                "task_describe":task.task_describe,
                "task_start_date":task.task_start_date,
                "task_end_date":task.task_end_date,
                "task_create_date":task.task_create_date,
                "task_type":task.task_type,
                "inform_type": task.inform_type
            })

        return DetailResponse(data=ret, msg="获取成功")    
    
    # 修改某个任务的信息，包含任务名称，任务描述，任务开始时间，任务结束时间，通知方式
    @action(methods=['POST'], detail=False, permission_classes=[])
    def modify_task(self, request: Request):
        task_id = request.data.get("task_id")
        if 'task_name' in request.data:
            Task.objects.filter(task_id=task_id).update(task_name=request.data.get("task_name"))

        if 'task_describe' in request.data:
            Task.objects.filter(task_id=task_id).update(task_describe=request.data.get("task_describe"))

        if 'task_start_date' in request.data:
            Task.objects.filter(task_id=task_id).update(task_start_date=request.data.get("task_start_date"))
        
        if 'task_end_date' in request.data:
            Task.objects.filter(task_id=task_id).update(task_end_date=request.data.get("task_end_date"))

        if 'inform_type' in request.data:
            Task.objects.filter(task_id=task_id).update(inform_type=request.data.get("inform_type"))

        return DetailResponse(data=[], msg="修改成功")  



