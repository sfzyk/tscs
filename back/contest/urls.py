from django.urls import path
from util.util import dispatch
from .views import *
from .state_change import *
from administrator.views import *
urlpatterns = [
    path('', dispatch(POST=add_contest)),
    path('contest/<int:index>/<int:pagesize>/', dispatch(POST=get_contest)),
    path('modify/', dispatch(POST=modify_contest)),
    path('delete/', dispatch(POST=delete_contest)),
    path('info/<int:contest_id>/', dispatch(GET=contest_info)),
    # 发送邮件
    path('finish_dispatch/<int:contest_id>/', dispatch(GET=start_finish_check)),

    path('publish/', dispatch(POST=publish_contest)),
    path('stop/', dispatch(POST=stop_contest)),
    path('finish/', dispatch(POST=finish_check_contest)),
    path('recheck/', dispatch(POST=wait_for_recheck)),

    path('enter_final/', dispatch(POST=enter_the_final_result)),
    path('stage_final/', dispatch(POST=stage_the_final_result)),
    path('get_final/', dispatch(POST=get_socre_winner)),

    path("a/", dispatch(GET=send_invitation)),
]