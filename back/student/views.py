from functools import reduce

from django.shortcuts import render
from django.http import JsonResponse
from util.util import parse_arg, ErrorCode, require_student_login, require_administor_login, project_get_student_name
from .models import *
from util.valid import *
from project.models import *
from django.core.exceptions import ObjectDoesNotExist
from contest.models import *
from django.db.models import Q
# Create your views here.


@require_student_login
def logout(request):
    del request.session['user']
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

    if valid_student_login(password=data['password'], user_email=data['email']):
        st = Student.objects.get(email=data['email'])
        request.session['user'] = {"email": data['email'],
                                   'id': st.id,
                                   'student_id': st.student_id,
                                   'name': st.name,
                                   'department': st.department,
                                   'major': st.major,
                                   'year': st.year,
                                   'telephone': st.telephone,
                                   'birth_date': str(st.birth_date)
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


@require_student_login
def get_user_info(request):
    item = ["email", 'id', 'student_id', 'name', 'department', 'major', 'year', 'telephone', 'birth_date']
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": {i: request.u[i] for i in item}
    })


def register(request):
    try:
        data = parse_arg(request.POST, ['email', 'password', 'id', 'name',
                                        'department', 'year', 'telephone', 'major', 'birth_date'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    if not valid_email(data['email']):
        return JsonResponse({
            "code": ErrorCode.EMAIL_INVALID,
            "data": ""
        })
    if not valid_telephone(data['telephone']):
        return JsonResponse({
            "code": ErrorCode.TELEPHONE_INVALID,
            "data": ""
        })
    if not valid_password(data['password']):
        return JsonResponse({
            "code": ErrorCode.PASSWORD_INVALID,
            "data": ""
        })
    if not valid_birth_date(data['birth_date']):
        return JsonResponse({
            "code": ErrorCode.BIRTHDATE_INVALID,
            "data": ""
        })
    if len(data['name']) == 0 or len(data['id']) == 0:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_INVALID,
            "data": ""
        })
    res = Student.objects.filter(email=data['email'])
    if len(res) >= 1:
        return JsonResponse({
            "code": ErrorCode.EMAIL_DUP,
            "data": ""
        })
    else:
        Student.objects.create(student_id=data['id'], email=data['email'], password=data['password'],
                               telephone=data['telephone'], name=data['name'], birth_date=data['birth_date'],
                               year=data['year'], major=data['major'], department=data['department']).save()
        return JsonResponse({
            "code": ErrorCode.ERROR_NON,
            "data": ""
        })


@require_student_login
def student_get_project_info(request, proj_id):
    try:
        project = Project.objects.get(id=proj_id, student_id=request.u['id'])
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.PROJECT_NOTEXIST,
            "data": ""
        })
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": project.object2json()
    })


@require_student_login
def modify_user_info(request):
    item = ['email', 'name', 'department', 'year', 'telephone', 'major', 'birth_date']
    st = Student.objects.get(id=request.u['id'])
    for i in item:
        if i in request.POST:
            st.__setattr__(i, request.POST[i])
            request.session['user'][i] = request.POST[i]
    request.session.modified = True
    st.save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })



@require_student_login
def get_project_list(request, index, pagesize):
    if not valid_page_index(index):
        return JsonResponse({
            "code": ErrorCode.PAGE_INVALID,
            "data": ""
        })
    if not valid_page_size(pagesize):
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

    project_list = Project.objects.filter(student_id=request.u['id'])
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
        project_list = project_list.filter(
            reduce(lambda x, y: x | y, [Q(**{i + "__contains": search['common_search']}) for i in str_item]))
    other_item = ['state', 'contest_id', 'expire', 'education_background', "category", "type", "id"]
    for i in str_item:
        if i in search:
            project_list = project_list.filter(**{i + "__contains": search[i]})
    for i in other_item:
        if i in search:
            project_list = project_list.filter(**{i: search[i]})

    object_num = (project_list.count() + pagesize - 1) // pagesize
    data = [project_get_student_name(i) for i in project_list[index * pagesize: (index + 1) * pagesize]]
    #print(data)
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": {
            "num": object_num,
            "data": data
        }
    })


@require_student_login
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
    contest_list = Contest.objects.filter(~Q(state=0))
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