from django.urls import path
from util.util import dispatch
from .views import *

urlpatterns = [
    path('project_stage/', dispatch(POST=save)),
    path('project_modify/', dispatch(POST=modify)),
    path('project_submit/', dispatch(POST=submit)),
    path('project_delete/', dispatch(POST=delete)),
]