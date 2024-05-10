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
from dvadmin.system.models import Users, Role, Dept, Department, EvaluateTask, Task, Staff, WeightTask, Rank, Department
from dvadmin.system.views.role import RoleSerializer
from dvadmin.utils.json_response import ErrorResponse, DetailResponse, SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.validator import CustomUniqueValidator
from dvadmin.utils.viewset import CustomModelViewSet
from dvadmin.utils.calc import calc_score, calc_relation
from dvadmin.utils.send_email import send_email
import numpy as np


class WeightTaskViewSet(CustomModelViewSet):

    queryset = WeightTask.objects.all()

    @action(methods=['POST'], detail=False, permission_classes=[])
    def weight_task_create(self, request: Request):
        task_id = uuid.uuid4()
        task_name = request.data.get("task_name")
        task_describe = request.data.get("task_describe")
        task_create_date = datetime.now()
        Task(task_id=task_id, task_name=task_name, task_describe=task_describe, task_create_date=task_create_date, task_type=1).save()
        staff_all = Staff.objects.all()
        department_all = Department.objects.all()
        department_list = []
        for department in department_all:
            if department.normal_department.startswith("B"):
                department_list.append(department.staff_department)

        for staff in staff_all:
            normal_department = Department.objects.get(staff_department=staff.staff_department).normal_department
            normal_rank = Rank.objects.get(staff_department=staff.staff_department, staff_rank=staff.staff_rank).normal_rank
            if normal_department.startswith("B") and int(normal_rank)==1:
                for department in department_list:
                    WeightTask(task_id=task_id, staff_id=staff.staff_id, evaluate_department=staff.staff_department, evaluated_department=department, weight_complete=0).save()


        return DetailResponse(data=dict(task_id=task_id), msg="创建成功")
    

    @action(methods=['POST'], detail=False, permission_classes=[])
    def weight_task_info(self, request: Request):
        task_id = request.data.get("task_id")
        staff_id = request.data.get("staff_id")
        evaluate = Staff.objects.get(staff_id=staff_id)
        department = evaluate.staff_department
        tasks = WeightTask.objects.filter(staff_id=staff_id, task_id=task_id)

        ret = []
        for task in tasks:
            if department != task.evaluated_department:
                ret.append(dict(evaluated_department=task.evaluated_department,weight=task.weight))
        
        return DetailResponse(data=ret, msg="获取成功")
    


    @action(methods=['POST'], detail=False, permission_classes=[])
    def submit_weight_task(self, request: Request):
        staff_id = request.data.get("staff_id")
        task_id = request.data.get("task_id")
        weights = request.data.get("weights")
        submit_type = request.data.get("submit_type")
        
        for weight in weights:
            evaluated_department = weight["evaluated_department"]
            WeightTask.objects.filter(staff_id=staff_id, task_id=task_id, evaluated_department=evaluated_department).update(weight=weight["weight"])
            
        if submit_type == 1:
            WeightTask.objects.filter(staff_id=staff_id, task_id=task_id).update(weight_complete=1)
            return DetailResponse(data=[], msg="提交成功")
        else:  
            return DetailResponse(data=[], msg="保存成功")

        
    
    @action(methods=['GET'], detail=False, permission_classes=[])
    def weight_task_status(self, request: Request):
        weight_task_count = Task.objects.filter(task_type=1).count()
        if weight_task_count == 0:
            return DetailResponse(data=dict(task_status=-1), msg="获取成功")
        else:
            weight_task_done = Task.objects.get(task_type=1).task_done
            if weight_task_done == 0:
                department_all = Department.objects.all()
                department_list = []
                for department in department_all:
                    if department.normal_department.startswith("B"):
                        department_list.append(department.staff_department)
                
                ret = []
                for department in department_list:
                    if WeightTask.objects.filter(evaluate_department=department).count() != 0:
                        completed = WeightTask.objects.filter(evaluate_department=department).first().weight_complete
                        ret.append(dict(department=department,completed=completed))
                
                return DetailResponse(data=dict(task_status=0, completed_list=ret), msg="获取成功")

            else:
                return DetailResponse(data=dict(task_status=1), msg="获取成功")

    @action(methods=['GET'], detail=False, permission_classes=[])
    def get_weight_matrix(self, request: Request):
        department_all = Department.objects.all()
        department_list = []
        for department in department_all:
            if department.normal_department.startswith("B"):
                department_list.append(department.staff_department)

        ret = {}
        for department in department_list:
            ret[department] = {}

        weight_task_all = WeightTask.objects.all()

        for weight_task in weight_task_all:
            ret[weight_task.evaluate_department][weight_task.evaluated_department] = weight_task.weight

        return DetailResponse(data=ret, msg="获取成功")
    
    @action(methods=['GET'], detail=False, permission_classes=[])
    def reset_weight_task(self, request: Request):
        Task.objects.filter(task_type=1).delete()
        WeightTask.objects.all().delete()

        return DetailResponse(data=[], msg="删除成功")
    
    @action(methods=['GET'], detail=False, permission_classes=[])
    def cal_weight_task(self, request: Request):
        task = Task.objects.get(task_type=1)
        task.task_done = 1
        task.save()
        task_id = Task.objects.get(task_type=1).task_id
        all_evaluate = list(WeightTask.objects.filter(task_id=task_id).values_list('evaluate_department', flat=True).distinct().order_by('evaluate_department'))
        all_evaluated = list(WeightTask.objects.filter(task_id=task_id).values_list('evaluated_department', flat=True).distinct().order_by('evaluated_department'))

        map_evaluate = {}
        map_evaluated = {}
        for index, evaluate_id in enumerate(all_evaluate):
            map_evaluate[evaluate_id] = index
        
        for index, evaluated_id in enumerate(all_evaluated):
            map_evaluated[evaluated_id] = index

        weights = np.zeros((len(all_evaluate), len(all_evaluated)))

        task_all = WeightTask.objects.all()
        for task in task_all:
            i = map_evaluate[task.evaluate_department]
            j = map_evaluated[task.evaluated_department]
            weights[i, j] = task.weight

        ret_weights = calc_relation(weights)

        for evaluate in all_evaluate:
            for evaluated in all_evaluated:
                WeightTask.objects.filter(evaluate_department=evaluate, evaluated_department=evaluated).update(weight=ret_weights[map_evaluate[evaluate]][map_evaluated[evaluated]])
        
        return DetailResponse(data=[], msg="计算成功")
                

    
     

    
    
    

        


    
        




