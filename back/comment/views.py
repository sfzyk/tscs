from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import render

from expert.models import Expert
from project.models import Project
#from util.util import require_expert_login, parse_arg, ErrorCode
from comment.models import *
# Create your views here.
from util.util import parse_arg, ErrorCode, require_expert_login
from util.valid import valid_score_check


@require_expert_login
@atomic
def make_comment(request):#保存不提交
    try:
        data = parse_arg(request.POST, ['project_id', 'comment', 'score'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    try:
        comment_to=Project.objects.get(id=data['project_id'])
        expert=Expert.objects.get(id=request.e['id'])
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.PROJECT_NOTEXIST,
            "data": ""
        })
    if not valid_score_check(data['score']):
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_INVALID,
            "data": ""
        })
    else:
        if Comment.objects.filter(Q(expert=expert)&Q(project=comment_to)).count()!=0:
            comment=Comment.objects.get(Q(expert=expert)&Q(project=comment_to))
            comment.comment=data['comment']
            comment.score=data['score']
            comment.save()
        else:
            Comment.objects.create(comment=data['comment'], score=data['score'], project=comment_to,expert=expert,state=0)
        return JsonResponse({
            "code": ErrorCode.ERROR_NON,
            "data": ""
        })


@require_expert_login
@atomic
def commit(request):
    try:
        project_id = parse_arg(request.POST, ['project_id'])['project_id']
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    try:
        expert = Expert.objects.get(id=request.e['id'])
        project = Project.objects.get(id=project_id)
        comment=Comment.objects.get(Q(project=project)&Q(expert=expert))
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.PROJECT_NOTEXIST,
            "data": ""
        })
    if (project.state!=2 and project.state!=3) or comment.state!=0:
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""
        })
    comment.state = 1
    comment.save()
    project.state=3
    project.save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON      ,
        "data": ""
    })


@require_expert_login
def getMyProjectComment(request):
    expert_id=request.e['id']
    try:
        project_id=parse_arg(request.POST,['project_id'])['project_id']
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    try:
        expert=Expert.objects.get(id=expert_id)
        project=Project.objects.get(id=project_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.PROJECT_NOTEXIST,
            "data": ""
        })
    if Comment.objects.filter(Q(expert=expert)&Q(project=project)).count() == 0:
        return JsonResponse({
            "code":ErrorCode.ERROR_NON,
            "data":{
                "comment": "",
                "score": 0,
                "state": 0
            }
        })
    else:
        comment=Comment.objects.get(Q(expert=expert) & Q(project=project))
        return JsonResponse({
            "code":ErrorCode.ERROR_NON,
            "data":{
                "comment":comment.comment,
                "score":comment.score,
                "state":comment.state
            }
        })