from django.urls import path
from .views import *
from util.util import dispatch

urlpatterns = [
    path('login/', dispatch(POST=login)),
    path('logout/', dispatch(POST=logout)),
    path('projects/<int:index>/<int:pagesize>/', dispatch(POST=get_project_list)),
    path('projects/<int:index>/<int:pagesize>/<int:contest_id>/', dispatch(POST=get_project_list)),
    path('project_info/<int:proj_id>/', dispatch(GET=adminsitor_get_project_info)),
    path('example_info/', dispatch(GET=get_example_expert_info)),
    path('load_expert/', dispatch(POST=load_expert_info)),
    path('load_experts/', dispatch(POST=load_experts_info)),
    path('modify_expert/', dispatch(POST=modify_expert_info)),
    path('delete_expert/', dispatch(POST=delete_expert_info)),
    path('delete_all_expert/', dispatch(POST=delete_all_expert_info)),
    path('review_project/', dispatch(POST=review_project)),
    path('revert_project/<int:proj_id>/', dispatch(GET=get_back_project)),
    path('zip_file/<int:contest_id>/', dispatch(GET=get_zip_file_by_contest)),
    path('comment/<int:proj_id>/', dispatch(GET=get_project_comments_info)),
    path('sys_info/', dispatch(GET=get_sys_info)),
    path('modify_sys_info/', dispatch(POST=modify_config))
]