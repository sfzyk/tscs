import random
from django.shortcuts import render
from comment.models import Comment
from util.util import *
from util.valid import *
from django.db.models import  Q
from django.core.exceptions import ObjectDoesNotExist
from contest.models import *
from project.models import *
from administrator.models import *
from .models import *
from django.db import transaction
from django.db.models import Q
from functools import reduce
from resource.models import *
from sendfile import sendfile


def parse_experts(ids):
    dict = json.loads(ids)
    red = reduce(lambda x, y: x | y, [Q(id=i) for i in dict])
    return Expert.objects.filter(red)


def create_reation(expert_list, proj, contest_id):
    for i in expert_list:
        if Expert_projects.objects.filter(expert_id=i.id, project_id=proj.id).count() > 0:
            exp = Expert.objects.filter(field=proj-1)
            expert_one = exp[random.randint(0, exp.count())]
            while Expert_projects.objects.filter(expert_id=expert_one.id, project_id=proj.id).count() > 0:
                expert_one = exp[random.randint(0, exp.count())]
            Expert_projects.objects.create(expert_id=expert_one.id, project_id=proj.id, contest_id=contest_id).save()
        else:
            Expert_projects.objects.create(expert_id=i.id, project_id=proj.id, contest_id=contest_id).save()


# 分配剩余专家完成任务
def auto_do_dispatch(contest_id, exp_objs):
    projects = Project.objects.filter(contest_id=contest_id)
    experts_per_proj = Config.objects.get(id=0).expert_per_proj
    count = 0
    for i in range(6):  # 对于每一个领域
        ps = projects.filter(category=i+1)
        es = exp_objs.filter(field=i)
 
        if es.count() < experts_per_proj and ps.count() > 0:
            return -1
        if es.count() == 0 and ps.count() == 0:
            continue
        ps_list = [i for i in ps]
        random.shuffle(ps_list)
        group_num = (es.count() + experts_per_proj - 1) // experts_per_proj  # 需要分配的组
        idx = 0
        projects_num = len(ps)
        if group_num == 0:
            return -1
        average = projects_num // group_num
        for j in range(group_num):
            for d in range(average):
                experts_g = es[j * experts_per_proj: (j + 1) * experts_per_proj]  # 当前的专家组成员
                num = Expert_projects.objects.filter(project_id=ps_list[idx].id).count()  # 这个项目已经有的专家数目
                experts_tmp = [i for i in experts_g]
                random.shuffle(experts_tmp)
                create_reation(experts_tmp[:experts_per_proj - num], ps_list[idx], contest_id)  # 创建关系
                count += experts_per_proj - num
                idx += 1
        experts_random = [i for i in es]
        for j in range(projects_num - group_num * average):
            random.shuffle(experts_random)
            num = Expert_projects.objects.filter(project_id=ps_list[idx].id).count()  # 这个项目已经有的专家数目
            create_reation(experts_random[:experts_per_proj - num], ps_list[idx], contest_id)
            #print(num)
            count += experts_per_proj - num
            idx += 1
    return count


@require_administor_login
@transaction.atomic
def auto_dispatch_expert(request, contest_id):
    try:
        contest = Contest.objects.get(id=contest_id)
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
    sp = transaction.savepoint()
    count = auto_do_dispatch(contest_id, Expert.objects)
    if count < 0:
        transaction.savepoint_rollback(sp)
        return JsonResponse({
            "code": ErrorCode.NEEDS_EXPERT,
            "data": ""
        })
    else:
        transaction.savepoint_commit(sp)
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": count
    })


@require_administor_login
def get_dispath_percent(request, contest_id):
    try:
        contest = Contest.objects.get(id=contest_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.CONTEST_NOTEXIST,
            "data": ""
        })
    exps = Expert_projects.objects.filter(contest_id=contest_id)
    projs = Project.objects.filter(Q(contest_id=contest_id) & (Q(state=2) | Q(state=3) | Q(state=4) | Q(state=5)))
    all_need_num = projs.count() * Config.objects.get(id=0).expert_per_proj
    if all_need_num == 0:
        return {
            "code": ErrorCode.ERROR_NON,
            "data": [0, 0, 0, 0]
        }
    percent = (exps.count() * 100) // all_need_num
    un_response = Expert_contests.objects.filter(state=0, contest_id=contest_id)
    accept = Expert_contests.objects.filter(state=1, contest_id=contest_id)
    refuse = Expert_contests.objects.filter(state=2, contest_id=contest_id)
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": [percent, un_response.count(), accept.count(), refuse.count()]
    })


@require_administor_login
@transaction.atomic
def dispatch_expert_by_hand(request):
    try:
        data = parse_arg(request.POST, ['ids', 'contest_id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    try:
        contest = Contest.objects.filter(id=data['contest_id'])
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.CONTEST_NOTEXIST,
            "data": ""
        })
    experts = parse_experts(data['ids'])
    sp = transaction.savepoint()
    count = auto_do_dispatch(data['contest_id'], experts)
    if count < 0:
        transaction.savepoint_rollback(sp)
        return JsonResponse({
            "code": ErrorCode.NEEDS_EXPERT,
            "data": ""
        })
    else:
        transaction.savepoint_commit(sp)
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": count
    })


@require_administor_login
def empty_expert_in_contest(request, contest_id):
    try:
        contest = Contest.objects.get(id=contest_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    Expert_projects.objects.filter(contest_id=contest_id).delete()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_administor_login
def delete_expert_projects(request):
    try:
        data = parse_arg(request.POST, ['expert_project_id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    Expert_projects.objects.filter(id=data['expert_project_id']).delete()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_administor_login
def add_expert_projects(request):
    try:
        data = parse_arg(request.POST, ['proj_id', 'expert_id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    if len(Expert_projects.objects.filter(project_id=data['proj_id'], expert_id=data['expert_id'])) > 0:
        return JsonResponse({
            "code": ErrorCode.EXPERT_DUPLICATE,
            "data": ""
        })
    proj_con_id = Project.objects.get(id=data['proj_id']).contest_id
    e_p = Expert_projects.objects.create(expert_id=data['expert_id'], project_id=data['proj_id'], contest_id=proj_con_id)
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": e_p.id
    })


@require_administor_login
def get_experts_list(request, index, pagesize, contest_id=-1):
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
    experts_list = Expert.objects.all()
    pre_fix = None
    if data['order'] == '2':
        pre_fix = "+"
    elif data['order'] == '1':
        pre_fix = "-"
    if pre_fix:
        if pre_fix == '+':
            pre_fix = ""
        experts_list = experts_list.order_by(pre_fix + data['field'])
    search = json.loads(data['search'])
    str_item = ["name", "email", "field", "college", 'telephone']
    if "common_search" in search:
        experts_list = experts_list.filter(**{i + "__contains": search['common_search'] for i in str_item})
    other_item = ['state']
    for i in str_item:
        if i in search:
            experts_list = experts_list.filter(**{i + "__contains": search[i]})
    for i in other_item:
        if i in search:
            experts_list = experts_list.filter(**{i: search[i]})
    object_num = (experts_list.count() + pagesize - 1) // pagesize
    if contest_id != -1:
        data = [i.objectcontest2json() for i in experts_list[index * pagesize: (index + 1) * pagesize]]
    else:
        data = [i.object2json() for i in experts_list[index * pagesize: (index + 1) * pagesize]]
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": {
            "num": object_num,
            "data": data
        }
    })


def logout(request):
    del request.session['e']
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

    if valid_expert_login(password=data['password'], user_email=data['email']):
        st = Expert.objects.get(email=data['email'])
        request.session['e'] = {"email": data['email'],
                                'id': st.id,
                                'name': st.name,
                                'college': st.college,
                                'telephone': st.telephone,
                                'field': st.field
                                }
        request.session.modified = True
        return JsonResponse({
            "code": ErrorCode.ERROR_NON,
            "data": ""
        })
    else:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_INVALID,
            "data": ""
        })


@require_expert_login
def modify_expert_info(request):
    try:
        expert = Expert.objects.get(request.e['id'])
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.EXPERT_NOTEXIST,
            "data": ""
        })
    item = ['name', 'password', 'college', 'telephone']
    for i in item:
        if i in request.POST:
            expert.__setattr__(i, request.POST[i])
            request.session[i] = request.POST[i]
    expert.save()
    request.session.modified = True
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


def get_invitation(request):
    try:
        data = parse_arg(request.POST, ['uni_link', 'accept'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })

    try:
        exp_con = Expert_contests.objects.get(session=data['uni_link'])
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.PERMISSION_DENIED,
            "data": ""
        })
    exp_con.session = ""
    if data['accept'] == 0:
        exp_con.state = 1
    else:
        exp_con.state = 2
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_expert_login
def get_expert_info(request):
    item = ["email", 'id',  'field', 'college', 'name', 'telephone']
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": {i: request.e[i] for i in item}
    })


@require_expert_login
def get_project_list(request, index, pagesize):
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
    project_list = [i.project_id for i in Expert_projects.objects.filter(expert_id=request.e['id'])]
    if len(project_list) == 0:
        return JsonResponse({
            "code": ErrorCode.ERROR_NON,
            "data": {
                "num": 0,
                "data": []
            }
        })
    project_list = Project.objects.filter(reduce(lambda x, y: x | y, [Q(id=i) for i in project_list]))

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
        project_list = project_list.filter(**{i+"__contains": search['common_search'] for i in str_item})
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


@require_expert_login
def get_project(request, proj_id):
    try:
        project = Project.objects.get(id=proj_id)
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.PROJECT_NOTEXIST,
            "data": ""
        })
    if Expert_projects.objects.filter(expert_id=request.e['id'], project_id=proj_id).count() == 0:
        return JsonResponse({
            "code": ErrorCode.PERMISSION_DENIED,
            "data": ""
        })

    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": project.object2json()
        })


@require_expert_login
def getMyComments(request):
    try:
        expert_id = request.e['id']
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    try:
        expert = Expert.objects.get(id=expert_id)
        my_comments_id = Comment.objects.filter(expert=expert).values("id")
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.CONTEST_NOTEXIST,
            "data": ""
        })
    result = [i['id'] for i in my_comments_id]
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": result
    })


def get_expert_register_info(request):
    try:
        data = parse_arg(request.POST, ['uni_link'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })

    req = Expert_contests.objects.filter(session=data['uni_link'])
    if req.count() == 0:
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""
        })
    re = req[0]
    exp_id = re.expert_id
    exp = Expert.objects.get(id=exp_id)
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": {
            "name": exp.name,
            "email": exp.email,
            "field": exp.field,
            "state": exp.state,
            "telephone": exp.telephone,
            "college": exp.college
        }
    })


def join_or_reject(request):
    try:
        data = parse_arg(request.POST, ['uni_link', 'join'])
    except KeyError:
        return JsonResponse({
            'code': ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    req = Expert_contests.objects.filter(session=data['uni_link'])
    if req.count() == 0:
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""
        })
    re = req[0]
    exp = Expert.objects.get(id=re.expert_id)
    if '0' == data['join']:
        re.state = 1
        if exp.state == 0:
            if "password" in request.POST:
                exp.password = request.POST['password']
            else:
                return JsonResponse({
                    "code": ErrorCode.ARGUMENT_NONEXIST,
                    "data": ""
                })
            request.session['e'] = {"email": exp.email,
                                    'id': exp.id,
                                    'name': exp.name,
                                    'college': exp.college,
                                    'telephone': exp.telephone,
                                    'field': exp.field
                                    }
        elif exp.state == 1:
            request.session['e'] = {"email": exp.email,
                                    'id': exp.id,
                                    'name': exp.name,
                                    'college': exp.college,
                                    'telephone': exp.telephone,
                                    'field': exp.field
                                    }
            request.e = request.session['e']
    else:
        re.state = 2
    re.session = ""
    exp.save()
    request.session.modified = True
    re.save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_expert_login
def get_all_expert_zip_file(request):
    file_name = get_contest_zip(request.e['id'])
    return sendfile(request, file_name, attachment=True)
