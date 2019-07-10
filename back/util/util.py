import json
from functools import wraps
from django.http import JsonResponse, HttpResponseNotAllowed
from django.http import QueryDict
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from smtplib import SMTP_SSL
from expert.models import  *



class ErrorCode:
    ERROR_NON = 200
    ARGUMENT_INVALID = 201  # 参数不合法
    ARGUMENT_EMPTY = 202  # 参数为空
    ARGUMENT_NONEXIST = 203  # 参数不存在

    EMAIL_INVALID = 204  # 邮箱不合法
    TELEPHONE_INVALID = 205  # 手机号不合法
    PASSWORD_INVALID = 206  # 密码不合法
    BIRTHDATE_INVALID = 209  # 出生日期不合法

    EMAIL_DUP = 207  # 邮箱重复
    NEEDS_LOGIN = 208  # 没有登录

    UNACCEPTABLE_OPERATING = 210  # 不可用的操作
    PERMISSION_DENIED = 211  # 越权操作

    PAGE_INVALID = 212  # 页码不合法

    JSON_ERROR = 241  # json格式不正确
    PROJECT_NOTEXIST = 242  # 项目不存在
    PROJECT_EXPIRE = 243  # 项目过期

    INVALID_EDUCATION = 244  # 教育背景不合法
    CONTEST_NOTEXIST = 245

    COMMENT_NOTEXIST = 246
    EXPERT_NOTEXIST = 247

    RESOURCE_TOOLARGE = 270
    TOOMANY_IMAGES = 271
    INVALID_IMAGE = 272

    IMAGE_NOTEXIST = 273
    DOCUMENT_NOTEXIST = 274
    INVALID_VIDEO = 275  # 估计永远也用不到
    VIDEO_NOTEXIST = 276

    EXPERT_DUPLICATE = 277  # 专家已经参与了那个评审
    NEEDS_EXPERT = 278
    STATE_ERROR = 279    # 竞赛等状态错误，无法进行某些操作
    PROJECT_NOTCOMMMENTED = 280

    UNKNOWN_ERROR = 299
def require_administor_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = args[0]
        if 'admin' not in auth.session:
            return JsonResponse({
                "code": ErrorCode.NEEDS_LOGIN,
                "data": ""
            })
        auth.u = auth.session['admin']
        return f(*args, **kwargs)
    return decorated


def require_student_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = args[0]
        if 'user' not in auth.session:
            return JsonResponse({
                "code": ErrorCode.NEEDS_LOGIN,
                "data": ""
            })
        auth.u = auth.session['user']
        return f(*args, **kwargs)
    return decorated


def require_expert_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = args[0]
        if 'e' not in auth.session:
            return JsonResponse({
                "code": ErrorCode.NEEDS_LOGIN,
                "data": ""
            })
        auth.e = auth.session['e']
        return f(*args, **kwargs)
    return decorated


def parse_put_arg(response_body, item):
    PUT = {k: v[0] if len(v) == 1 else v for k, v in QueryDict(response_body).lists()}
    print(PUT)
    ret = {}
    for i in item:
        if i not in PUT:
            raise KeyError
        else:
            ret[i] = PUT[i]
    return ret


def parse_arg(response_body, item):
    args = response_body
    ret = {}
    for i in item:
        if i not in args:
            raise KeyError
        else:
            ret[i] = args[i]
    return ret


def dispatch(**methods):
    def invalid_handler(request, *args, **kwargs):
        return HttpResponseNotAllowed(methods.keys())

    def handler(request, *args, **kwargs):
        view = methods.get(request.method, invalid_handler)
        return view(request, *args, **kwargs)
    return handler


def administrator_project_get(e):
    exps = Expert_projects.objects.filter(project_id=e.id)
    ret = {i.id: (i.expert_id, i.expert.name) for i in exps}
    return {
        "student_name": e.student.name,
        "id": e.id,
        "full_name": e.full_name,
        "category": e.category,
        "state": e.state,
        "expire": e.expire,
        "contest_id": e.contest_id,
        "contest_name": e.contest.name if e.contest else "",
        "expert_info": ret
    }


def project_get_student_name(e):
    return {
        "student_name": e.student.name,
        "id": e.id,
        "full_name": e.full_name,
        "category": e.category,
        "state": e.state,
        "expire": e.expire,
        "contest_id": e.contest_id,
        "contest_name": e.contest.name,
    }


def fieldstr2int(f):
    ret = -1
    if f == "机械与控制               ":
        ret = 0
    elif f == '信息技术':
        ret = 1
    elif f == '数理':
        ret = 2
    elif f == '生命科学':
        ret = 3
    elif f == '能源化工':
        ret = 4
    elif f == '哲学社会科学':
        ret = 5
    else:
        print(f)
        raise ValueError
    return ret


def send_invation__(to, content):
    f = open("/home/git/summer_work/util/mail.json", "r")
    mail_info = json.loads(f.read())
    smtp = SMTP_SSL(mail_info["hostname"])
    smtp.ehlo(mail_info["hostname"])
    smtp.login(mail_info["username"], mail_info["password"])
    msg = MIMEText(content, "html", mail_info["mail_encoding"])
    msg["Subject"] = Header("邀请你参加评审工作",  mail_info["mail_encoding"])
    msg["from"] = mail_info["from"]
    msg["to"] = to
    smtp.sendmail(mail_info["from"], to, msg.as_string())
    smtp.quit()