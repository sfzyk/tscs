from django.urls import path

from notice.views import createNotice, getNotice, getAttach, delNotice, getNoticeList
from util.util import dispatch

urlpatterns = [
    path('add_notice/',dispatch(POST=createNotice)),
    path('get_notice/',dispatch(POST=getNotice)),
    path('get_attach/',dispatch(GET=getAttach)),
    path('delete_notice/',dispatch(POST=delNotice)),
    path('get_list/',dispatch(POST=getNoticeList))
]