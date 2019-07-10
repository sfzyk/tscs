from functools import reduce

from django.shortcuts import render
from util.util import *
from .models import *
from expert.models import *
from django.core.exceptions import ObjectDoesNotExist
from util.valid import *
from django.db.models import Q
from sendfile import sendfile
from project.models import Project
from comment.models import *
import uuid
import datetime


@require_administor_login
def get_contest(request, index, pagesize):
    if not valid_page_index(index):
        if not valid_page_index(index):
            return JsonResponse({
                "code": ErrorCode.PAGE_INVALID,
                "data": ""
            })
    try:
        data = parse_arg(request.POST, ['field', 'search', 'order'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    contest_list = Contest.objects.all()
    pre_fix = None
    if data['order'] == '2':
        pre_fix = "+"
    elif data['order'] == '1':
        pre_fix = "-"
    if pre_fix:
        if pre_fix == '+':
            pre_fix = ""
        contest_list = contest_list.order_by(pre_fix + data['field'])
    search = json.loads(data['search'])
    str_item = ["name", "descriptions", "expire_date", "checkin_expire_date"]
    if "common_search" in search:
        contest_list = contest_list.filter(
            reduce(lambda x, y: x | y, [Q(**{i + "__contains": search['common_search']}) for i in str_item]))
    other_item = ['state', 'id']
    for i in str_item:
        if i in search:
            contest_list = contest_list.filter(**{i + "__contains": search[i]})
    for i in other_item:
        if i in search:
            contest_list = contest_list.filter(**{i: search[i]})
    object_num = (contest_list.count() + pagesize - 1) // pagesize
    data = [i.object2json() for i in contest_list[index * pagesize: (index + 1) * pagesize]]
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": {
            "num": object_num,
            "data": data
        }
    })


@require_administor_login
def add_contest(request):
    try:
        data = parse_arg(request.POST, ['descriptions', 'name', 'expire_date', 'stop_date'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    Contest.objects.create(descriptions=data['descriptions'],
                           name=data['name'], state=0,
                           expire_date=data['expire_date'],
                           checkin_expire_date=data['stop_date']).save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_administor_login
def delete_contest(request):
    try:
        data = parse_arg(request.POST, ['contest_id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    Contest.objects.filter(id=data['contest_id']).delete()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_administor_login
def modify_contest(request):
    try:
        data = parse_arg(request.POST, ['contest_id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    try:
        contest = Contest.objects.get(id=data['contest_id'])
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.CONTEST_NOTEXIST,
            "data": ""
        })
    modify_info =request.POST
    item = ['name', 'descriptions', 'expire_date', 'checkin_expire_date']
    for i in item:
        if i in modify_info:
            contest.__setattr__(i, modify_info[i])
    contest.save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })




def contest_info(request, contest_id):
    try:
        contest = Contest.objects.get(id=contest_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.CONTEST_NOTEXIST,
            'data': ""
        })
    project_list = Project.objects.filter(contest_id=contest_id)
    project_num = project_list.count()
    project_st0 = project_list.filter(state=0).count()
    project_st1 = project_list.filter(state=1).count()
    project_st2 = project_list.filter(state=2).count()
    project_st3 = project_list.filter(state=3).count()
    project_st4 = project_list.filter(state=4).count()
    project_st5 = project_list.filter(state=5).count()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": {
            "contest_info": contest.object2json(),
            "detail_info": [project_num, project_st0, project_st1, project_st2, project_st3, project_st4, project_st5]
        }
    })


def send_invitation(email, uni_link, contest, num_projs, name):
    info = """尊敬的{}老师您好：    
    近期为提升学生创新能力，举办了新一届科技竞赛{}，现邀请您进行评审其中{}个项目。
    查看邀请请点击链接{} (该链接一次点击失效)
    """
    link = "http://59.110.224.120/invitation/" + uni_link
    info = info.format(name, contest.name, num_projs, link)
    send_invation__(email, info)
    return 0

# 专家分配完成，开始初审，发送邮件
@require_administor_login
def start_finish_check(request, contest_id):
    try:
        contest = Contest.objects.get(id=contest_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.CONTEST_NOTEXIST,
            "data": ""
        })
    all_experts = Expert_projects.objects.filter(contest_id=contest_id)
    joined_experts = Expert_contests.objects.filter(Q(contest_id=contest_id) & (Q(state=0) | Q(state=1)))
    joined_experts_id = set([i.expert_id for i in joined_experts])  # 已经加入该竞赛的专家Id
    count = 0
    error = 0
    #print(joined_experts_id)
    for i in all_experts:
        if i.expert_id not in joined_experts_id:  # 新加入该竞赛的专家
            uni_link = uuid.uuid4()
            num_proj = Expert_projects.objects.filter(expert_id=i.expert_id, contest_id=contest_id).count()
            tm = send_invitation(i.expert.email, str(uni_link), contest, num_proj, i.expert.name)
            if tm == -1: #错误发送
                error += 1
            else:  # 成功发送
                Expert_contests.objects.create(expert_id=i.expert_id, contest_id=contest_id, state=0,
                                               session=str(uni_link)).save()
            count += 1
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": error
    })


