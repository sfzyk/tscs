from django.shortcuts import render
from util.util import *
from util.valid import *
from django.http import JsonResponse
from student.models import Student
from .models import Project, Cooperator
from django.db import transaction
from django.db.models import ObjectDoesNotExist
from json.decoder import JSONDecodeError
import json


@require_student_login
@transaction.atomic
def save(request):  # 保存而不提交
    try:  # 验证基础参数
        data = parse_arg(request.POST, ['full_name', 'telephone', 'email', 'cooperator_info', 'contest_id',
                                        'type', 'type_info','address', 'innovation', 'keywords',
                                        'category', 'descriptions', 'education_background'])
    except KeyError:
        return JsonResponse({"code": ErrorCode.ARGUMENT_NONEXIST,
                             "data": ""})
    # 解析合作者名单
    try:
        cooperators = json.loads(data['cooperator_info'])
    except JSONDecodeError:
        return JsonResponse({
            "code": ErrorCode.JSON_ERROR,
            "data": ""
            }
        )

    for i in cooperators:  # 检查合作者格式正确
        if not valid_cooperator(cooperators):
            return JsonResponse({
                "code": ErrorCode.ARGUMENT_INVALID,
                "data": ""
            })
    # 开始创建新的项目
    proj = Project.objects.create(full_name=data['full_name'],
                                  telephone=data['telephone'],
                                  address=data['address'],
                                  email=data['email'],
                                  keywords=data['keywords'],
                                  category=data['category'],
                                  descriptions=data['descriptions'],
                                  innovation=data['innovation'],
                                  student_id=request.u['id'],
                                  birth_date=request.u['birth_date'],
                                  education_background=data['education_background'],
                                  state=0,
                                  expire=0,
                                  name=request.u['name'],
                                  year=request.u['year'],
                                  major=request.u['major'],
                                  type=data['type'],
                                  type_info=data['type_info'],
                                  contest_id=data['contest_id']
                                  )
    proj.save()
    for i in cooperators:  # 创建每一个合作者
        try:
            data = parse_arg(json.loads(cooperators[i]), ['name', 'email', 'student_id', 'telephone', 'education_background'])
        except KeyError:
            return JsonResponse({
                "code": ErrorCode.ARGUMENT_NONEXIST,
                "data": ""
            })
        except JSONDecodeError:
            return JsonResponse({
                "code": ErrorCode.JSON_ERROR,
                "data": ""
            })
        Cooperator.objects.create(name=data['name'], email=data['email'], telephone=data['telephone'], project=proj,
                                  student_id=data['student_id'], education_background=data['education_background']).save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": proj.id,
    })


@require_student_login
@transaction.atomic
def modify(request):  # 修改而不提交
    try:
        data = parse_arg(request.POST, ['info', 'id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    try:  # 解析这个数据
        modify_info = json.loads(data['info'])
        if 'cooperator_info' in modify_info:  # 确定要修改这些和作业
            modify_cooperator = modify_info['cooperator_info']
            for i in modify_cooperator:
                modify_cooperator[i] = json.loads(modify_cooperator[i])
    except JSONDecodeError:
        return JsonResponse({
            "code": ErrorCode.JSON_ERROR,
            "data": ""
        })

    proj_id = data['id']

    try:
        proj = Project.objects.get(id=proj_id, student=request.u['id'])  # 获取这个proj 需要是这个项目的作者
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.PROJECT_NOTEXIST,
            "data": ""
        })
    if proj.state != 0:
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""
        })
    if proj.expire != 0:
        return JsonResponse({
            "code": ErrorCode.PROJECT_EXPIRE,
            "data": ""
        })

    if 'education_background' in modify_info and not valid_education_background(str(modify_info['education_background'])):
        return JsonResponse({
            "code": ErrorCode.INVALID_EDUCATION,
            "data": ""
        })

    # 修改这个项目的属性
    items = ['full_name', 'telephone', 'address', 'email', 'category', 'keywords', 'type', 'type_info',
             'descriptions', 'innovation', 'student_id', 'birth_date',
             'education_background', 'contest_id']

    for i in items:
        if i in modify_info:
            proj.__setattr__(i, modify_info[i])
    proj.save()

    if 'cooperator_info' in modify_info:   # 需要修改合作者
        Cooperator.objects.filter(project=proj_id).delete()
        for i in modify_cooperator:  # 创建每一个合作者
            try:
                parse_arg(modify_cooperator[i], ['name', 'email', 'student_id',
                                                 'telephone', 'education_background'])
            except KeyError:
                return JsonResponse({
                    "code": ErrorCode.ARGUMENT_NONEXIST,
                    "data": ""
                })
        for i in modify_cooperator:
            data = parse_arg(modify_cooperator[i], ['name', 'email', 'student_id', 'telephone', 'education_background'])
            Cooperator.objects.create(name=data['name'], email=data['email'],
                                      student_id=data['student_id'], telephone=data['telephone'],
                                      education_background=data['education_background'], project=proj)
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_student_login
def submit(request):  # 提交
    try:
        data = parse_arg(request.POST, ['proj_id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })

    try:
        proj = Project.objects.get(id=data['proj_id'], student=request.u['id'])  # 获取这个proj 需要是这个项目的作者
    except ObjectDoesNotExist:
        return JsonResponse({
            "code": ErrorCode.PROJECT_NOTEXIST,
            "data": ""
        })

    if proj.state != 0:
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""
        })
    if proj.expire != 0:
        return JsonResponse({
            "code": ErrorCode.PROJECT_EXPIRE,
            "data": ""
        })
    proj.state = 1
    proj.save()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })


@require_student_login
def delete(request):
    try:
        data = parse_arg(request.POST, ['proj_id'])
    except KeyError:
        return JsonResponse({
            "code": ErrorCode.ARGUMENT_NONEXIST,
            "data": ""
        })
    res = Project.objects.filter(id=data['proj_id'])
    if len(res) == 0:
        return JsonResponse({
            "code": ErrorCode.PROJECT_NOTEXIST,
            "data": ""
        })
    if res[0].state != 0:
        return JsonResponse({
            "code": ErrorCode.UNACCEPTABLE_OPERATING,
            "data": ""
        })

    res.delete()
    return JsonResponse({
        "code": ErrorCode.ERROR_NON,
        "data": ""
    })
