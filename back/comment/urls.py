from django.urls import path

from comment.views import make_comment, commit, getMyProjectComment
from expert.views import getMyComments
from util.util import dispatch

urlpatterns = [
    path('comment_stage/',dispatch(POST=make_comment)),
    path('comment_submit/',dispatch(POST=commit)),
    path('project_comment/',dispatch(POST=getMyProjectComment))
]