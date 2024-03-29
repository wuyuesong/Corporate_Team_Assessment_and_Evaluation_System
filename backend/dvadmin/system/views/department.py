# # -*- coding: utf-8 -*-

# """
# @author: wys
# @contact: QQ:1377030423
# @Remark: 部门管理
# """
# from rest_framework import serializers
# from rest_framework.decorators import action
# from rest_framework.permissions import IsAuthenticated

# from dvadmin.system.models import Department, RoleMenuButtonPermission, Users
# from dvadmin.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
# from dvadmin.utils.serializers import CustomModelSerializer
# from dvadmin.utils.viewset import CustomModelViewSet


# class DeptSerializer(CustomModelSerializer):
#     """
#     部门-序列化器
#     """
#     parent_name = serializers.CharField(read_only=True, source='parent.staff_department')
#     status_label = serializers.SerializerMethodField()
#     has_children = serializers.SerializerMethodField()
#     hasChild = serializers.SerializerMethodField()

#     dept_user_count = serializers.SerializerMethodField()


#     class Meta:
#         model = Department
#         fields = '__all__'
#         read_only_fields = ["id"]


# class DeptImportSerializer(CustomModelSerializer):
#     """
#     部门-导入-序列化器
#     """

#     class Meta:
#         model = Department
#         fields = '__all__'
#         read_only_fields = ["id"]


# class DeptCreateUpdateSerializer(CustomModelSerializer):
#     """
#     部门管理 创建/更新时的列化器
#     """

#     def create(self, validated_data):
#         value = validated_data.get('parent', None)
#         if value is None:
#             validated_data['parent'] = self.request.user.dept
#         dept_obj = Department.objects.filter(parent=self.request.user.dept).order_by('-sort').first()
#         last_sort = dept_obj.sort if dept_obj else 0
#         validated_data['sort'] = last_sort + 1
#         instance = super().create(validated_data)
#         instance.dept_belong_id = instance.id
#         instance.save()
#         return instance

#     class Meta:
#         model = Department
#         fields = '__all__'


# class DeptViewSet(CustomModelViewSet):
#     """
#     部门管理接口
#     list:查询
#     create:新增
#     update:修改
#     retrieve:单例
#     destroy:删除
#     """
#     queryset = Department.objects.all()
#     serializer_class = DeptSerializer
#     create_serializer_class = DeptCreateUpdateSerializer
#     update_serializer_class = DeptCreateUpdateSerializer
#     filter_fields = ['name', 'id', 'parent']
#     search_fields = []
#     # extra_filter_class = []
#     import_serializer_class = DeptImportSerializer
#     import_field_dict = {
#         "staff_department": "部门名称",
#         "normal_departmemt": "部门标准化",
#     }

#     def list(self, request, *args, **kwargs):
#         # 如果懒加载，则只返回父级
#         request.query_params._mutable = True
#         params = request.query_params
#         parent = params.get('parent', None)
#         page = params.get('page', None)
#         limit = params.get('limit', None)
#         if page:
#             del params['page']
#         if limit:
#             del params['limit']
#         if params and parent:
#             queryset = self.queryset.filter(status=True, parent=parent)
#         else:
#             queryset = self.queryset.filter(status=True)
#         queryset = self.filter_queryset(queryset)
#         serializer = DeptSerializer(queryset, many=True, request=request)
#         data = serializer.data
#         return SuccessResponse(data=data)

#     @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated], extra_filter_class=[])
#     def dept_lazy_tree(self, request, *args, **kwargs):
#         parent = self.request.query_params.get('parent')
#         is_superuser = request.user.is_superuser
#         if is_superuser:
#             queryset = Dept.objects.values('id', 'name', 'parent')
#         else:
#             role_ids = request.user.role.values_list('id', flat=True)
#             data_range = RoleMenuButtonPermission.objects.filter(role__in=role_ids).values_list('data_range', flat=True)
#             user_dept_id = request.user.dept.id
#             dept_list = [user_dept_id]
#             data_range_list = list(set(data_range))
#             for item in data_range_list:
#                 if item in [0, 2]:
#                     dept_list = [user_dept_id]
#                 elif item == 1:
#                     dept_list = Dept.recursion_all_dept(dept_id=user_dept_id)
#                 elif item == 3:
#                     dept_list = Dept.objects.values_list('id', flat=True)
#                 elif item == 4:
#                     dept_list = request.user.role.values_list('dept', flat=True)
#                 else:
#                     dept_list = []
#             queryset = Dept.objects.filter(id__in=dept_list).values('id', 'name', 'parent')
#         return DetailResponse(data=queryset, msg="获取成功")

#     @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated], extra_filter_class=[])
#     def all_dept(self, request, *args, **kwargs):
#         queryset = self.filter_queryset(self.get_queryset())
#         data = queryset.filter(status=True).order_by('sort').values('name', 'id', 'parent')
#         return DetailResponse(data=data, msg="获取成功")

#     @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
#     def move_up(self, request):
#         """部门上移"""
#         dept_id = request.data.get('dept_id')
#         try:
#             dept = Dept.objects.get(id=dept_id)
#         except Dept.DoesNotExist:
#             return ErrorResponse(msg="部门不存在")
#         previous_menu = Dept.objects.filter(sort__lt=dept.sort, parent=dept.parent).order_by('-sort').first()
#         if previous_menu:
#             previous_menu.sort, dept.sort = dept.sort, previous_menu.sort
#             previous_menu.save()
#             dept.save()
#         return SuccessResponse(data=[], msg="上移成功")

#     @action(methods=['POST'], detail=False, permission_classes=[IsAuthenticated])
#     def move_down(self, request):
#         """部门下移"""
#         dept_id = request.data['dept_id']
#         try:
#             dept = Dept.objects.get(id=dept_id)
#         except Dept.DoesNotExist:
#             return ErrorResponse(msg="部门不存在")
#         next_menu = Dept.objects.filter(sort__gt=dept.sort, parent=dept.parent).order_by('sort').first()
#         if next_menu:
#             next_menu.sort, dept.sort = dept.sort, next_menu.sort
#             next_menu.save()
#             dept.save()
#         return SuccessResponse(data=[], msg="下移成功")

#     @action(methods=['GET'], detail=False, permission_classes=[])
#     def dept_info(self, request):
#         """部门信息"""
#         def inner(did, li):
#             sub = Dept.objects.filter(parent_id=did)
#             if not sub.exists():
#                 return li
#             for i in sub:
#                 li.append(i.pk)
#                 inner(i, li)
#             return li
#         dept_id = request.query_params.get('dept_id')
#         show_all = request.query_params.get('show_all')
#         if dept_id is None:
#             return ErrorResponse(msg="部门不存在")
#         if not show_all:
#             show_all = 0
#         if int(show_all):  # 递归当前部门下的所有部门，查询用户
#             all_did = [dept_id]
#             inner(dept_id, all_did)
#             users = Users.objects.filter(dept_id__in=all_did)
#         else:
#             if dept_id != '':
#                 users = Users.objects.filter(dept_id=dept_id)
#             else:
#                 users = Users.objects.none()
#         dept_obj = Dept.objects.get(id=dept_id) if dept_id != '' else None
#         sub_dept = Dept.objects.filter(parent_id=dept_obj.pk) if dept_id != '' else []
#         data = {
#             'dept_name': dept_obj and dept_obj.name,
#             'dept_user': users.count(),
#             'owner': dept_obj and dept_obj.owner,
#             'description': dept_obj and dept_obj.description,
#             'gender': {
#                 'male': users.filter(gender=1).count(),
#                 'female': users.filter(gender=2).count(),
#                 'unknown': users.filter(gender=0).count(),
#             },
#             'sub_dept_map': []
#         }
#         for dept in sub_dept:
#             all_did = [dept.pk]
#             inner(dept.pk, all_did)
#             sub_data = {
#                 'name': dept.name,
#                 'count': Users.objects.filter(dept_id__in=all_did).count()
#             }
#             data['sub_dept_map'].append(sub_data)
#         return SuccessResponse(data)

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


class DepartmentCreateSerializer(CustomModelSerializer):
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
        model = Department
        fields = "__all__"
        # read_only_fields = ["id"]
        # extra_kwargs = {
        #     "post": {"required": False},
        #     "mobile": {"required": False},
        # }


class DepartmentUpdateSerializer(CustomModelSerializer):
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
        model = Department
        # read_only_fields = ["id"]
        fields = "__all__"
        # extra_kwargs = {
        #     "post": {"required": False, "read_only": True},
        #     "mobile": {"required": False},
        # }


class DepartmentInfoUpdateSerializer(CustomModelSerializer):
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
        model = Department
        fields = "__all__"
        # exclude = ['id']
        # extra_kwargs = {
        #     "post": {"required": False, "read_only": True},
        #     "mobile": {"required": False},
        # }


class ExportDepartmentProfileSerializer(CustomModelSerializer):
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
        model = Department
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


class DepartmentProfileImportSerializer(CustomModelSerializer):
    # password = serializers.CharField(read_only=True, required=False)

    def save(self, **kwargs):
        data = super().save(**kwargs)
        # password = hashlib.new(
        #     "md5", str(self.initial_data.get("password", "admin123456")).encode(encoding="UTF-8")
        # ).hexdigest()
        # data.set_password(password)
        data.save()
        return data

    class Meta:
        model = Department
        fields = "__all__"
        # exclude = (
        #     "post",
        #     "user_permissions",
        #     "groups",
        #     "is_superuser",
        #     "date_joined",
        # )


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
    filter_fields = "__all__"
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
    # import_field_dict = {
    #     "username": "登录账号",
    #     "name": "用户名称",
    #     "email": "用户邮箱",
    #     "mobile": "手机号码",
    #     "gender": {
    #         "title": "用户性别",
    #         "choices": {
    #             "data": {"未知": 2, "男": 1, "女": 0},
    #         }
    #     },
    #     "is_active": {
    #         "title": "帐号状态",
    #         "choices": {
    #             "data": {"启用": True, "禁用": False},
    #         }
    #     },
    #     "dept": {"title": "部门", "choices": {"queryset": Dept.objects.filter(status=True), "values_name": "name"}},
    #     "role": {"title": "角色", "choices": {"queryset": Role.objects.filter(status=True), "values_name": "name"}},
    # }
    import_field_dict = {
        "staff_department": "部门名称",
        "normal_department": "标准化部门"
    }

    def Department_delete_all(self, request: Request):
        Department_all = Department.objects.all()
        Department_all.delete()
        return DetailResponse(data=[], msg="删除成功")

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

