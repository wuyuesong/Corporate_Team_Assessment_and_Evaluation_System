from django.urls import path
from rest_framework import routers

from dvadmin.system.views.api_white_list import ApiWhiteListViewSet
from dvadmin.system.views.area import AreaViewSet
from dvadmin.system.views.clause import PrivacyView, TermsServiceView
from dvadmin.system.views.dept import DeptViewSet
from dvadmin.system.views.dictionary import DictionaryViewSet
from dvadmin.system.views.file_list import FileViewSet
from dvadmin.system.views.login_log import LoginLogViewSet
from dvadmin.system.views.menu import MenuViewSet
from dvadmin.system.views.menu_button import MenuButtonViewSet
from dvadmin.system.views.message_center import MessageCenterViewSet
from dvadmin.system.views.operation_log import OperationLogViewSet
from dvadmin.system.views.role import RoleViewSet
from dvadmin.system.views.role_menu import RoleMenuPermissionViewSet
from dvadmin.system.views.role_menu_button_permission import RoleMenuButtonPermissionViewSet
from dvadmin.system.views.system_config import SystemConfigViewSet
from dvadmin.system.views.user import UserViewSet
from dvadmin.system.views.menu_field import MenuFieldViewSet
from dvadmin.system.views.staff import StaffViewSet
from dvadmin.system.views.rank import RankViewSet
from dvadmin.system.views.department import DepartmentViewSet
from dvadmin.system.views.evaluate_task import EvaluateTaskViewSet
from dvadmin.system.views.task import TaskViewSet
from dvadmin.system.views.weight_task import WeightTaskViewSet

system_url = routers.SimpleRouter()
system_url.register(r'menu', MenuViewSet)
system_url.register(r'menu_button', MenuButtonViewSet)
system_url.register(r'role', RoleViewSet)
system_url.register(r'dept', DeptViewSet)
system_url.register(r'user', UserViewSet)
system_url.register(r'operation_log', OperationLogViewSet)
system_url.register(r'dictionary', DictionaryViewSet)
system_url.register(r'area', AreaViewSet)
system_url.register(r'file', FileViewSet)
system_url.register(r'api_white_list', ApiWhiteListViewSet)
system_url.register(r'system_config', SystemConfigViewSet)
system_url.register(r'message_center', MessageCenterViewSet)
system_url.register(r'role_menu_button_permission', RoleMenuButtonPermissionViewSet)
system_url.register(r'role_menu_permission', RoleMenuPermissionViewSet)
system_url.register(r'column', MenuFieldViewSet)


system_url.register(r'staff', StaffViewSet)
system_url.register(r'rank', RankViewSet)
system_url.register(r'department', DepartmentViewSet)
system_url.register(r'evaluate_task', EvaluateTaskViewSet)
system_url.register(r'task', TaskViewSet)
system_url.register(r'weight_task', WeightTaskViewSet)



urlpatterns = [
    path('user/export/', UserViewSet.as_view({'post': 'export_data', })),
    path('user/import/', UserViewSet.as_view({'get': 'import_data', 'post': 'import_data'})),
    path('staff/delete_all/', StaffViewSet.as_view({'get': 'staff_delete_all',})),
    path('staff/generate_account/', StaffViewSet.as_view({'get': 'generate_account',})),
    path('rank/delete_all/', RankViewSet.as_view({'get': 'rank_delete_all',})),
    path('rank/unique_rank_list/', RankViewSet.as_view({'get': 'unique_rank_list',})),
    path('rank/tree_rank_list/', RankViewSet.as_view({'get': 'tree_rank_list',})),
    path('department/delete_all/', DepartmentViewSet.as_view({'get': 'department_delete_all',})),
    path('evaluate_task/evaluate_task_create/', EvaluateTaskViewSet.as_view({'post': 'evaluate_task_create',})),
    # path('evaluate_task/evaluate_task_info/', EvaluateTaskViewSet.as_view({'post': 'evaluate_task_info',})),
    # path('evaluate_task/submit_evaluate_task/', EvaluateTaskViewSet.as_view({'post': 'submit_evaluate_task',})),
    # path('task/task_list/', TaskViewSet.as_view({'post': 'task_list',})),

    path('system_config/save_content/', SystemConfigViewSet.as_view({'put': 'save_content'})),
    path('system_config/get_association_table/', SystemConfigViewSet.as_view({'get': 'get_association_table'})),
    path('system_config/get_table_data/<int:pk>/', SystemConfigViewSet.as_view({'get': 'get_table_data'})),
    path('system_config/get_relation_info/', SystemConfigViewSet.as_view({'get': 'get_relation_info'})),
    path('login_log/', LoginLogViewSet.as_view({'get': 'list'})),
    path('login_log/<int:pk>/', LoginLogViewSet.as_view({'get': 'retrieve'})),
    path('dept_lazy_tree/', DeptViewSet.as_view({'get': 'dept_lazy_tree'})),
    path('clause/privacy.html', PrivacyView.as_view()),
    path('clause/terms_service.html', TermsServiceView.as_view()),
]
urlpatterns += system_url.urls
