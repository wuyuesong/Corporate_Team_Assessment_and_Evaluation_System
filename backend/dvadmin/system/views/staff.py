import hashlib, random, string, os
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.hashers import make_password, check_password
from django_restql.fields import DynamicSerializerMethodField
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from django.db import connection
from django.db.models import Q
from application import dispatch
from dvadmin.system.models import Users, Role, Dept, Staff, Department, Rank, EvaluateTask, WeightTask, Task
from dvadmin.system.views.role import RoleSerializer
from dvadmin.utils.json_response import ErrorResponse, DetailResponse, SuccessResponse
from dvadmin.utils.serializers import CustomModelSerializer
from dvadmin.utils.validator import CustomUniqueValidator
from dvadmin.utils.viewset import CustomModelViewSet
from django.db import transaction


# def recursion(instance, parent, result):
#     new_instance = getattr(instance, parent, None)
#     res = []
#     data = getattr(instance, result, None)
#     if data:
#         res.append(data)
#     if new_instance:
#         array = recursion(new_instance, parent, result)
#         res += array
#     return res


class StaffSerializer(CustomModelSerializer):
    """
    用户管理-序列化器
    """
    # dept_name = serializers.CharField(source='dept.name', read_only=True)
    # role_info = DynamicSerializerMethodField()
    # dept_name_all = serializers.SerializerMethodField()

    class Meta:
        model = Staff
        fields = "__all__"
        # read_only_fields = ["id"]
        # exclude = ["password"]
        # extra_kwargs = {
        #     "post": {"required": False},
        #     "mobile": {"required": False},
        # }

    # def get_dept_name_all(self, instance):
    #     dept_name_all = recursion(instance.dept, "parent", "name")
    #     dept_name_all.reverse()
    #     return "/".join(dept_name_all)

    # def get_role_info(self, instance, parsed_query):
    #     roles = instance.role.all()
    #     # You can do what ever you want in here
    #     # `parsed_query` param is passed to BookSerializer to allow further querying
    #     serializer = RoleSerializer(
    #         roles,
    #         many=True,
    #         parsed_query=parsed_query
    #     )
    #     return serializer.data


class StaffCreateSerializer(CustomModelSerializer):
    """
    用户新增-序列化器
    """

    # username = serializers.CharField(
    #     max_length=50,
    #     validators=[
    #         CustomUniqueValidator(queryset=Users.objects.all(), message="账号必须唯一")
    #     ],
    # )
    # password = serializers.CharField(
    #     required=False,
    # )

    # def validate_password(self, value):
    #     """
    #     对密码进行验证
    #     """
    #     md5 = hashlib.md5()
    #     md5.update(value.encode('utf-8'))
    #     md5_password = md5.hexdigest()
    #     return make_password(md5_password)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        # data.dept_belong_id = data.dept_id
        data.save()
        # data.post.set(self.initial_data.get("post", []))
        return data

    class Meta:
        model = Staff
        fields = "__all__"
        # read_only_fields = ["id"]
        # extra_kwargs = {
        #     "post": {"required": False},
        #     "mobile": {"required": False},
        # }


class StaffUpdateSerializer(CustomModelSerializer):
    """
    用户修改-序列化器
    """

    # username = serializers.CharField(
    #     max_length=50,
    #     validators=[
    #         CustomUniqueValidator(queryset=Users.objects.all(), message="账号必须唯一")
    #     ],
    # )

    # password = serializers.CharField(required=False, allow_blank=True)
    # mobile = serializers.CharField(
    #     max_length=50,
    #     validators=[
    #         CustomUniqueValidator(queryset=Users.objects.all(), message="手机号必须唯一")
    #     ],
    #     allow_blank=True
    # )

    def save(self, **kwargs):
        data = super().save(**kwargs)
        # data.dept_belong_id = data.dept_id
        data.save()
        # data.post.set(self.initial_data.get("post", []))
        return data

    class Meta:
        model = Staff
        # read_only_fields = ["id"]
        fields = "__all__"
        # extra_kwargs = {
        #     "post": {"required": False, "read_only": True},
        #     "mobile": {"required": False},
        # }


class StaffInfoUpdateSerializer(CustomModelSerializer):
    """
    用户修改-序列化器
    """
    # mobile = serializers.CharField(
    #     max_length=50,
    #     validators=[
    #         CustomUniqueValidator(queryset=Users.objects.all(), message="手机号必须唯一")
    #     ],
    #     allow_blank=True
    # )

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = Staff
        fields = "__all__"
        # exclude = ['id']
        # extra_kwargs = {
        #     "post": {"required": False, "read_only": True},
        #     "mobile": {"required": False},
        # }


class ExportStaffProfileSerializer(CustomModelSerializer):
    """
    用户导出 序列化器
    """

    # last_login = serializers.DateTimeField(
    #     format="%Y-%m-%d %H:%M:%S", required=False, read_only=True
    # )
    # is_active = serializers.SerializerMethodField(read_only=True)
    # dept_name = serializers.CharField(source="dept.name", default="")
    # dept_owner = serializers.CharField(source="dept.owner", default="")
    # gender = serializers.CharField(source="get_gender_display", read_only=True)

    # def get_is_active(self, instance):
    #     return "启用" if instance.is_active else "停用"

    class Meta:
        model = Staff
        fields = "__all__"
        # fields = (
        #     "username",
        #     "name",
        #     "email",
        #     "mobile",
        #     "gender",
        #     "is_active",
        #     "last_login",
        #     "dept_name",
        #     "dept_owner",
        # )


class StaffProfileImportSerializer(CustomModelSerializer):
    # password = serializers.CharField(read_only=True, required=False)

    def save(self, **kwargs):
        data = super().save(**kwargs)

        try:
            Department.objects.get(staff_department=data.staff_department)
        except ObjectDoesNotExist:
            return f"{data.staff_department}部门不存在"
        
        try:
            Rank.objects.get(staff_rank=data.staff_rank, staff_department=data.staff_department)
        except ObjectDoesNotExist:
            return f"{data.staff_department}部门或{data.staff_department}部门中的{data.staff_rank}职级不存在" 
        
        data.save()    
        return data

    class Meta:
        model = Staff
        fields = "__all__"
        # exclude = (
        #     "post",
        #     "user_permissions",
        #     "groups",
        #     "is_superuser",
        #     "date_joined",
        # )


def get_normal_department(department):
    return Department.objects.get(staff_department=department).normal_department.zfill(2)

def get_normal_rank(rank, department):
    return Rank.objects.get(staff_rank=rank, staff_department=department).normal_rank.zfill(2)

def generate_password():
    length = 13
    chars = string.ascii_letters + string.digits + '!@#$%^&*()'
    random.seed = (os.urandom(1024))
    return ''.join(random.choice(chars) for i in range(length))

class StaffViewSet(CustomModelViewSet):
    """
    用户接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    create_serializer_class = StaffCreateSerializer
    update_serializer_class = StaffUpdateSerializer
    # filter_fields = ["name", "username", "gender", "is_active", "dept", "user_type"]
    # filter_fields = "__all__"
    filter_fields = ["staff_department",
        "staff_name",
        "staff_rank",
        "staff_job",
        "staff_title",
        "staff_kpi1",
        "staff_kpi2",
        "staff_kpi2",
        "assessment1",
        "assessment2",
        "assessment3",
        "staff_status",
        "staff_firm_id",
        "staff_telephone",
        "staff_email"]
    # search_fields = ["username", "name", "dept__name", "role__name"]
    search_fields = "__all__"
    # 导出
    export_field_label = {
        "staff_department": "单位名称",
        "staff_name": "员工姓名",
        "staff_rank": "职位等级",
        "staff_job": "岗位等级",
        "staff_title": "职称",
        "staff_kpi1": "第一年KPI",
        "staff_kpi2": "第二年KPI",
        "staff_kpi2": "第三年KPI",
        "assessment1": "第一年考核结果",
        "assessment2": "第二年考核结果",
        "assessment3": "第三年考核结果",
        "staff_status": "政治面貌",
        "staff_firm_id": "员工企业id",
        "staff_telephone": "员工电话",
        "staff_email": "员工邮箱",
        "username": "登录账号",
        "password": "登录密码"
    }
    export_serializer_class = ExportStaffProfileSerializer
    # 导入
    import_serializer_class = StaffProfileImportSerializer

    import_field_dict = {
        # "staff_department": {"title": "单位名称", "choices": {"queryset": Department.objects.all(), "values_name": "staff_department"}},
        "staff_department": "单位名称",
        "staff_name": "员工姓名",
        #"staff_rank": {"title": "职位等级", "choices": {"queryset": Rank.objects.all(), "values_name": "staff_rank"}},
        "staff_rank": "职位等级",
        "staff_job": "岗位等级",
        "staff_title": "职称",
        "staff_kpi1": "第一年KPI",
        "staff_kpi2": "第二年KPI",
        "staff_kpi3": "第三年KPI",
        "assessment1": "第一年考核结果",
        "assessment2": "第二年考核结果",
        "assessment3": "第三年考核结果",
        "staff_status": "政治面貌",
        "staff_firm_id": "员工企业id",
        "staff_telephone": "员工电话",
        "staff_email": "员工邮箱"
    }

    #删除所有员工信息
    def staff_delete_all(self, request: Request):
        Staff_all = Staff.objects.all()
        Staff_all.delete()

        evaluateTask_all = Staff.objects.all()
        evaluateTask_all.delete()

        WeightTask = Staff.objects.all()
        WeightTask.delete()

        Task = Staff.objects.all()
        Task.delete()
        
        staff_user_all = Users.objects.filter(our_user_type=2)
        staff_user_all.delete()
        
        return DetailResponse(data=[], msg="删除成功")
    
    # 生成账号接口
    # 加上锁，如果期间有报错，则回退，不然再次录入时主键会重复
    @transaction.atomic
    def generate_account(self, request: Request):
        Staff_all = Staff.objects.all()
        for staff in Staff_all:
            try:
                Department.objects.get(staff_department=staff.staff_department)
            except ObjectDoesNotExist:
                return ErrorResponse(msg=f"{staff.staff_name}  {staff.staff_department}部门不存在")
            normal_department = get_normal_department(staff.staff_department)
            
            try:
                Rank.objects.get(staff_rank=staff.staff_rank, staff_department=staff.staff_department)
            except ObjectDoesNotExist:
                return ErrorResponse(msg=f"{staff.staff_name}  {staff.staff_department}部门或{staff.staff_department}部门中的{staff.staff_rank}职级不存在")
            normal_rank = get_normal_rank(staff.staff_rank, staff.staff_department)
            staff.staff_id = normal_department + normal_rank + staff.staff_firm_id.zfill(6)
            staff.username = staff.staff_id
            staff.password = generate_password()
            Users(our_user_type=2, username=staff.username, raw_password=staff.password, staff_id=staff.staff_id).save()
            staff.save()
        return DetailResponse(data=[], msg="创建账号成功")
    
    # 已弃用
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        try:
            Department.objects.get(staff_department=serializer.data["staff_department"])
        except ObjectDoesNotExist:
            return ErrorResponse(msg=f"{serializer.data['staff_department']}部门不存在")
        
        try:
            Rank.objects.get(staff_rank=serializer.data['staff_rank'], staff_department=serializer.data["staff_department"])
        except ObjectDoesNotExist:
            return ErrorResponse(msg=f"{serializer.data['staff_department']}部门或{serializer.data['staff_department']}部门中的{serializer.data['staff_rank']}职级不存在")
        
        self.perform_create(serializer)
        return DetailResponse(data=serializer.data, msg="新增成功")




    # @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    # def user_info(self, request):
    #     """获取当前用户信息"""
    #     user = request.user
    #     result = {
    #         "id": user.id,
    #         "username": user.username,
    #         "name": user.name,
    #         "mobile": user.mobile,
    #         "user_type": user.user_type,
    #         "gender": user.gender,
    #         "email": user.email,
    #         "avatar": user.avatar,
    #         "dept": user.dept_id,
    #         "is_superuser": user.is_superuser,
    #         "role": user.role.values_list('id', flat=True),
    #     }
    #     if hasattr(connection, 'tenant'):
    #         result['tenant_id'] = connection.tenant and connection.tenant.id
    #         result['tenant_name'] = connection.tenant and connection.tenant.name
    #     dept = getattr(user, 'dept', None)
    #     if dept:
    #         result['dept_info'] = {
    #             'dept_id': dept.id,
    #             'dept_name': dept.name
    #         }
    #     else:
    #         result['dept_info'] = {
    #             'dept_id': None,
    #             'dept_name': "暂无部门"
    #         }
    #     role = getattr(user, 'role', None)
    #     if role:
    #         result['role_info'] = role.values('id', 'name', 'key')
    #     return DetailResponse(data=result, msg="获取成功")

    # @action(methods=["PUT"], detail=False, permission_classes=[IsAuthenticated])
    # def update_user_info(self, request):
    #     """修改当前用户信息"""
    #     serializer = UserInfoUpdateSerializer(request.user, data=request.data, request=request)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return DetailResponse(data=None, msg="修改成功")

    # @action(methods=["PUT"], detail=False, permission_classes=[IsAuthenticated])
    # def change_password(self, request, *args, **kwargs):
    #     """密码修改"""
    #     data = request.data
    #     old_pwd = data.get("oldPassword")
    #     new_pwd = data.get("newPassword")
    #     new_pwd2 = data.get("newPassword2")
    #     if old_pwd is None or new_pwd is None or new_pwd2 is None:
    #         return ErrorResponse(msg="参数不能为空")
    #     if new_pwd != new_pwd2:
    #         return ErrorResponse(msg="两次密码不匹配")
    #     verify_password = check_password(old_pwd, self.request.user.password)
    #     if not verify_password:
    #         verify_password = check_password(hashlib.md5(old_pwd.encode(encoding='UTF-8')).hexdigest(), self.request.user.password)
    #     if verify_password:
    #         request.user.password = make_password(hashlib.md5(new_pwd.encode(encoding='UTF-8')).hexdigest())
    #         request.user.save()
    #         return DetailResponse(data=None, msg="修改成功")
    #     else:
    #         return ErrorResponse(msg="旧密码不正确")

    # @action(methods=["PUT"], detail=True, permission_classes=[IsAuthenticated])
    # def reset_to_default_password(self, request, *args, **kwargs):
    #     """恢复默认密码"""
    #     instance = Users.objects.filter(id=kwargs.get("pk")).first()
    #     if instance:
    #         instance.set_password(dispatch.get_system_config_values("base.default_password"))
    #         instance.save()
    #         return DetailResponse(data=None, msg="密码重置成功")
    #     else:
    #         return ErrorResponse(msg="未获取到用户")

    # @action(methods=["PUT"], detail=True)
    # def reset_password(self, request, pk):
    #     """
    #     密码重置
    #     """
    #     if not self.request.user.is_superuser:
    #         return ErrorResponse(msg="只允许超级管理员对其进行密码重置")
    #     instance = Users.objects.filter(id=pk).first()
    #     data = request.data
    #     new_pwd = data.get("newPassword")
    #     new_pwd2 = data.get("newPassword2")
    #     if instance:
    #         if new_pwd != new_pwd2:
    #             return ErrorResponse(msg="两次密码不匹配")
    #         else:
    #             instance.password = make_password(new_pwd)
    #             instance.save()
    #             return DetailResponse(data=None, msg="修改成功")
    #     else:
    #         return ErrorResponse(msg="未获取到用户")

    # def list(self, request, *args, **kwargs):
    #     dept_id = request.query_params.get('dept')
    #     show_all = request.query_params.get('show_all')
    #     if not dept_id:
    #         dept_id = ''
    #     if not show_all:
    #         show_all = 0
    #     if int(show_all):
    #         all_did = [dept_id]
    #         def inner(did):
    #             sub = Dept.objects.filter(parent_id=did)
    #             if not sub.exists():
    #                 return
    #             for i in sub:
    #                 all_did.append(i.pk)
    #                 inner(i)
    #         if dept_id != '':
    #             inner(dept_id)
    #             searchs = [
    #                 Q(**{f+'__icontains':i})
    #                 for f in self.search_fields
    #             ] if (i:=request.query_params.get('search')) else []
    #             q_obj = []
    #             if searchs:
    #                 q = searchs[0]
    #                 for i in searchs[1:]:
    #                     q |= i
    #                 q_obj.append(Q(q))
    #             queryset = Users.objects.filter(*q_obj, dept_id__in=all_did)
    #         else:
    #             queryset = self.filter_queryset(self.get_queryset())
    #     else:
    #         queryset = self.filter_queryset(self.get_queryset())
    #     page = self.paginate_queryset(queryset)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True, request=request)
    #         return self.get_paginated_response(serializer.data)
    #     serializer = self.get_serializer(queryset, many=True, request=request)
    #     return SuccessResponse(data=serializer.data, msg="获取成功")
