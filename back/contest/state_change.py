from django.shortcuts import render
from util.util import *
from .models import *
from expert.models import *
from django.core.exceptions import ObjectDoesNotExist
from comment.models import *
from util.valid import *
from django.db.models import Q
from sendfile import sendfile
from project.models import Project
import uuid

@require_administor_login
def publish_contest(request):
    try:
        data = parse_arg(request.POST, ['contest_id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ERROR_NON,
            "data": ""
        })
    try:
        contest = Contest.objects.get(id=data['contest_id'])
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.CONTEST_NOTEXIST,
            "data": ""
        })
    if contest.state != 0:
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""
        })
    contest.state = 1
    contest.save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })

@require_administor_login
def stop_contest(request):
    try:
        data = parse_arg(request.POST, ['contest_id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ERROR_NON,
            "data": ""
        })
    try:
        contest = Contest.objects.get(id=data['contest_id'])
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.CONTEST_NOTEXIST,
            "data": ""
        })
    if contest.state != 1:
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""
        })
    contest.state = 2
    contest.save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })

# 专家评审中
@require_administor_login
def finish_check_contest(request):
    try:
        data = parse_arg(request.POST, ['contest_id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ERROR_NON,
            "data": ""
        })
    try:
        contest = Contest.objects.get(id=data['contest_id'])
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.CONTEST_NOTEXIST,
            "data": ""
        })
    if contest.state != 2:
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""
        })
    contest.state = 3
    contest.save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


# 等待校团委筛选中
@require_administor_login
def wait_for_recheck(request):
    try:
        data = parse_arg(request.POST, ['contest_id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ERROR_NON,
            "data": ""
        })
    try:
        contest = Contest.objects.get(id=data['contest_id'])
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.CONTEST_NOTEXIST,
            "data": ""
        })
    if contest.state != 3:
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""
        })
    projs = Project.objects.filter(contest_id=contest.id, state=2)


    Comment.objects.filter()
    contest.state = 4
    contest.save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })