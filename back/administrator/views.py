from functools import reduce
from statistics import mean

from django.core import serializers
from django.db.models import Q, Avg
from django.forms import model_to_dict
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.transaction import atomic
from comment.models import *
from util.util import *
from .models import *
from project.models import *
from util.valid import *
from expert.models import *
from sendfile import sendfile
from resource.models import get_zip_by_contest
import json
import xlrd


def logout(request):
    del request.session['admin']
    return JsonResponse({
        "code": 200,
        "data": ""
    })


def login(request):
    try:
        data = parse_arg(request.POST, ['email', 'password'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })

    if valid_administrators_login(password=data['password'], user_email=data['email']):
        adm = Administrator.objects.get(email=data['email'])
        request.session['admin'] = {"email": data['email'], 'id': adm.id}
        return JsonResponse({
            "code": ErrorCode.ERROR_NON,
            "data": ""
        })
    else:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_INVALID,
            "data": ""
        })


@require_administor_login
@atomic
def review_project(request):
    try:
        data = parse_arg(request.POST, ['proj_id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    try:
        proj = Project.objects.get(id=data['proj_id'])
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.ERROR_NON,
            "data": ""
        })

    if proj.expire != 0:
        return JsonResponse({
            "code": ErrorCode.PROJECT_EXPIRE,
            "data": ""
        })
    if proj.state != 1:
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""
        })
    Project.objects.filter(id=data['proj_id']).update(state=2)
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_administor_login
def get_project_list(request, index, pagesize, contest_id=-1):
    if not valid_page_index(index):
        return JsonResponse({
            "code": ErrorCode.PAGE_INVALID,
            "data": ""
        })
    try:
        data = parse_arg(request.POST, ['field', 'order', 'search'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    if contest_id == -1:
        project_list = Project.objects.filter(~Q(state=0))
    else:
        project_list = Project.objects.filter(~Q(state=0) & Q(contest_id=contest_id))
    pre_fix = None
    if data['order'] == '2':
        pre_fix = "+"
    elif data['order'] == '1':
        pre_fix = "-"
    if pre_fix:
        if pre_fix == '+':
            pre_fix = ""
        project_list = project_list.order_by(pre_fix + data['field'])

    search = json.loads(data['search'])
    str_item = ["innovation", "descriptions", "email", "telephone", "name", "keywords", 'full_name', "contest__name"]
    if "common_search" in search:
        project_list = project_list.filter(reduce(lambda x, y: x | y, [Q(**{i+"__contains":search['common_search']}) for i in str_item]))
    other_item = ['state', 'contest_id', 'expire', 'education_background', "category", "type", "id"]
    for i in str_item:
        if i in search:
            project_list = project_list.filter(**{i+"__contains": search[i]})
    for i in other_item:
        if i in search:
            project_list = project_list.filter(**{i: search[i]})

    object_num = (project_list.count() + pagesize - 1)//pagesize
    data = [administrator_project_get(i) for i in project_list[index*pagesize: (index+1)*pagesize]]
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": {
            "num": object_num,
            "data": data
        }
    })


@require_administor_login
def adminsitor_get_project_info(request, proj_id):
    try:
        project = Project.objects.get(id=proj_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.PROJECT_NOTEXIST,
            "data": ""
        })
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": project.admin_object2json()
    })


@require_administor_login
def get_sys_info(request):
    config = Config.objects.get(id=0)
    item = ["expert_per_proj", "num_proj"]
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": {i: config.__getattribute__(i) for i in item}
    })


@require_administor_login
def modify_config(request):
    config = Config.objects.get(id=0)
    item = ["expert_per_proj", "num_proj"]
    for i in item:
        auto = request.POST.get(i, None)
        if auto:
            config.__setattr__(i, auto)
    config.save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_administor_login
def get_example_expert_info(request):
    file = "resource/专家信息录入表.xlsx"
    return sendfile(request, file, attachment=False)


@require_administor_login
def load_expert_info(request):
    try:
        data = parse_arg(request.POST, ['email', 'field'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    if duplicate_email(data['email']):
        return JsonResponse({
            "code": ErrorCode.EMAIL_DUP,
            "data": ""
        })
    name = request.POST.get('name', "default")
    password = "no"
    field = data['field']
    state = 0
    telephone = request.POST.get("telephone", "default")
    email = data['email']
    college = request.POST.get("college", "default")
    Expert.objects.create(email=email, name=name, field=field, telephone=telephone,college=college, state=state, password=password).save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_administor_login
def load_experts_info(request):
    try:
        data = parse_arg(request.FILES, ['file'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })

    d = data['file'].read()
    book = xlrd.open_workbook(file_contents=d)
    sheet = book.sheet_by_index(0)
    l = len(sheet.col_values(0))
    error_num = 0
    for i in range(l-1):
        email = sheet.col_values(0)[i+1]
        if email == '':
            break
        field = fieldstr2int(sheet.col_values(1)[i+1])
        college = sheet.col_values(2)[i + 1]
        name = sheet.col_values(3)[i+1]
        telephone = sheet.col_values(4)[i+1]
        password = "default"
        if duplicate_email(email) or not valid_email(email):
            error_num += 1
        else:
            Expert.objects.create(email=email, name=name, field=field, telephone=telephone, college=college, state=0,
                              password=password).save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": error_num
    })


@require_administor_login
def modify_expert_info(request):
    try:
        data = parse_arg(request.POST, ['expert_id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    try:
        expert = Expert.objects.get(id=data['expert_id'])
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.EXPERT_NOTEXIST,
            "data": ""
        })
    item = ['name', 'password', 'college', 'telephone']
    for i in item:
        if i in request.POST:
            expert.__setattr__(i, request.POST[i])
    expert.save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_administor_login
def delete_all_expert_info(request):
    Expert.objects.all().delete()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_administor_login
def delete_expert_info(request):
    try:
        data = parse_arg(request.POST, ['expert_id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    Expert.objects.filter(id=data['expert_id']).delete()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_administor_login
def get_back_project(request, proj_id):
    try:
        proj = Project.objects.get(id=proj_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.PROJECT_NOTEXIST,
            "data": ""
        })
    if proj.state != 1:
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""
        })
    proj.state = 0
    proj.save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_administor_login
def get_socre_winner(request):
    try:
        contest_id = parse_arg(request.POST, ['contest_id'])['contest_id']
        num = Config.objects.get(id=0).num_proj
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    #判断contest状态
    try:
        contest = Contest.objects.get(id=contest_id)
        contest_state = contest.state
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.PROJECT_NOTEXIST,
            "data": ""
        })

    if contest_state != 4:
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""
        })

    all_project = Project.objects.filter(contest_id=contest_id)
    score = []
    for i in all_project:
        res = Comment.objects.filter(project_id=i.id, state=1)
        if res.count() == 0:
            return JsonResponse({
                "code": ErrorCode.PROJECT_NOTCOMMMENTED,
                "data": ""
            })
        s = mean([i.score for i in res])
        score.append([i.id, s, 0, i.full_name])
    score = sorted(score, key=lambda x: -x[1])
    if FinalStage.objects.filter(contest_id=contest_id).count() > 0:
        a = FinalStage.objects.get(contest_id=contest_id).result
        ids = set(json.loads(a))
        for idx, i in enumerate(score):
            if i[0] in ids:
                score[idx][2] = 1
    else:
        num = min(num, len(score))
        for i in range(num):
            score[i][2] = 1

    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": score
    })


@require_administor_login
def stage_the_final_result(request):
    try:
        data = parse_arg(request.POST, ['ids', 'contest_id'])
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
    if FinalStage.objects.filter(contest_id=data['contest_id']).count() > 0:
        FinalStage.objects.get(contest_id=data['contest_id'], result=data['ids'])
    else:
        FinalStage.objects.create(contest_id=data['contest_id'], result=data['ids'])
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_administor_login
def enter_the_final_result(request):
    try:
        data = parse_arg(request.POST, ['ids', 'contest_id'])
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
    ids = json.loads(data['ids'])
    if contest.state != 4:
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""})
    contest.state = 5
    contest.save()
    Project.objects.filter(state=3).update(state=5)
    for i in ids:
        p = Project.objects.get(id=i)
        p.state = 4
        p.save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data" : ""
    })


# 暂时不用
@require_administor_login
def get_project_comments_info(request, proj_id):
    try:
        proj = Project.objects.get(id=proj_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.PROJECT_NOTEXIST,
            "data": ""
        })
    coms = Comment.objects.filter(Q(project_id=proj_id) & (Q(state=1)))
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": [i.object2json() for i in coms]
    })


@require_administor_login
def get_zip_file_by_contest(request, contest_id):
    file_name = get_zip_by_contest(contest_id)
    if file_name == "":
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""
        })
    return sendfile(request, file_name, attachment=True)

