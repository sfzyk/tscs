from django.urls import path
from .views import *
from util.util import dispatch

urlpatterns = [
    path('logout/', dispatch(POST=logout)),
    path('login/', dispatch(POST=login)),
    path('register/', dispatch(POST=register)),
    path('project_info/<int:proj_id>/', dispatch(GET=student_get_project_info)),
    path('user_info/', dispatch(GET=get_user_info, POST=modify_user_info)),
    path('projects/<int:index>/<int:pagesize>/', dispatch(POST=get_project_list)),
    path('contests/<int:index>/<int:pagesize>/', dispatch(POST=get_contest))
]