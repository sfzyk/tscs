import json
import time

from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import atomic
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from sendfile import sendfile

from notice.models import Notice
from util.util import parse_arg, ErrorCode, require_administor_login

MAX_DOCUMENT_SIZE = 20*1024*1024  # 20M


#@require_administor_login
@atomic
def createNotice(request):
    try:
        data = parse_arg(request.POST, ['content', 'title'])
    except KeyError:
        return JsonResponse({
                "code": ErrorCode.ARGUMENT_NONEXIST,
                "data": ""
        })
    if "attach" in request.FILES:
        attach=parse_arg(request.FILES,['attach'])['attach']
        if attach.size>MAX_DOCUMENT_SIZE:
            return JsonResponse({
                "code": ErrorCode.RESOURCE_TOOLARGE,
                "data": ""
            })
        Notice.objects.create(attach=attach,title=data['title'],content=data['content'],time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))).save()
        return JsonResponse({
            "code":ErrorCode.ERROR_NON,
            "data":""
        })
    else:
        Notice.objects.create(title=data['title'], content=data['content'],time=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))).save()
        return JsonResponse({
            "code": ErrorCode.ERROR_NON,
            "data": ""
        })


def getNotice(request):
    try:
        id=parse_arg(request.POST,['notice_id'])['notice_id']
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    try:
        notice=Notice.objects.get(id=id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.EXPERT_NOTEXIST,
            "data": ""
        })
    result={
        "code":ErrorCode.ERROR_NON,
        "data":{
            "title":notice.title,
            "content":notice.content,
            "time":str(notice.time).split(" ")[0]
        }
    }
    if notice.attach!="":
        result['data']['attach']=notice.attach.name
    return JsonResponse(result)


def getAttach(request):
    try:
        notice_id=parse_arg(request.GET, ['notice_id'])['notice_id']
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    try:
        attach=Notice.objects.get(id=notice_id).attach
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.EXPERT_NOTEXIST,
            "data": ""
        })
    return sendfile(request=request, filename=attach.path, attachment=True,attachment_filename=attach)


def delNotice(request):
    try:
        notice_id=parse_arg(request.POST, ['notice_id'])['notice_id']
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    try:
        Notice.objects.filter(id=notice_id).delete()
    except:  # 目前未知
        return JsonResponse({
            "code": ErrorCode.UNKNOWN_ERROR,
            "data": ""
        })
    return JsonResponse({
        "code":ErrorCode.ERROR_NON,
        "data":""
    })


def getNoticeList(request):
    all_notice=Notice.objects.all().order_by("-time")
    result=[n.object2json() for i,n in  enumerate(all_notice)]
    return JsonResponse({
        "code":ErrorCode.ERROR_NON,
        "data":result
    })