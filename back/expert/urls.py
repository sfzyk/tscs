from django.urls import path
from django.views.generic import TemplateView
from .views import *
from util.util import dispatch

urlpatterns = [
    path('login/', dispatch(POST=login)),
    path('user_info/', dispatch(GET=get_expert_info)),
    path('logout/', dispatch(POST=logout)),
    path('modify/', dispatch(POST=modify_expert_info)),
    path('experts/<int:index>/<int:pagesize>/', dispatch(POST=get_experts_list)),
    path('experts_contests/<int:index>/<int:pagesize>/<contest_id>/', dispatch(POST=get_experts_list)),
    path('add_to_project/', dispatch(POST=add_expert_projects)),
    path('delete/', dispatch(POST=delete_expert_projects)),
    path('auto_dispatch/<int:contest_id>/', dispatch(GET=auto_dispatch_expert)),
    path('manual_dispatch/', dispatch(POST=dispatch_expert_by_hand)),
    path('resest_dispatch/<int:contest_id>/', dispatch(GET=empty_expert_in_contest)),
    path('dispath_percent/<int:contest_id>/', dispatch(GET=get_dispath_percent)),
    path('projects/<int:index>/<int:pagesize>/', dispatch(POST=get_project_list)),
    path('project/<int:proj_id>/', dispatch(GET=get_project)),
    path('zip_file/', dispatch(GET=get_all_expert_zip_file)),
    path('my_comments/', dispatch(POST=getMyComments)),

    path('invitation/info/', dispatch(POST=get_expert_register_info)),
    path('invitation/rest/', dispatch(POST=join_or_reject)),


]