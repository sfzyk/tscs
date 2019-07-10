from administrator.models import Administrator
from student.models import Student
from expert.models import Expert
import re


def valid_page_index(index):
    return 0 <= index


def valid_page_size(size):
    return 0 < size


def valid_birth_date(birth_date):
    if re.match(r"\d{4}-\d{2}-\d{2}", birth_date):
        return True
    else:
        return False


def valid_education_background(e_b):
    if re.match(r'0|1|2|3|4', e_b):
        return True
    return False


def valid_cooperator(co):
    return True


def valid_expert_login(user_email, password):
    try:
        expert = Expert.objects.get(email=user_email)
        if expert.password == password:
            return True
        else:
            return False
    except:
        return False


def valid_administrators_login(user_email, password):
    try:
        adm = Administrator.objects.get(email=user_email)
        if adm.password == password:
            return True
        else:
            return False
    except:
        return False


def valid_email(e):
    if re.match(r'^[0-9a-zA-Z\_\-]+(\.[0-9a-zA-Z\_\-]+)*@[0-9a-zA-Z]+(\.[0-9a-zA-Z]+)+$', e):
        return True
    else:
        return False


def valid_password(p):
    return True


def valid_student_login(user_email, password):
    try:
        stu = Student.objects.get(email=user_email)
        if stu.password == password:
            return True
        else:
            return False
    except:
        return False


def valid_telephone(t):
    if re.match(r'[0-9]+', t):
        return True
    else:
        return False


def valid_score_check(i):
    try:
        i=float(i)
        if i < 0 or i > 10:
            return False
        else:
            return True
    except:
        return False