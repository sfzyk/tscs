from django.db import models
import json
import django.utils.timezone as timezone
from contest.models import *
from expert.models import *

class Cooperator(models.Model):
    class Meta:
        db_table = "Cooperator"
    name = models.CharField(max_length=512)
    student_id = models.CharField(max_length=512)
    education_background = models.IntegerField()  #  0, 1, 2, 3
    telephone = models.CharField(max_length=56)
    email = models.CharField(max_length=56)
    project = models.ForeignKey(to="Project", on_delete=models.CASCADE)

    def object2json(self):
        return json.dumps({
            "name": self.name,
            "student_id": self.student_id,
            "education_background": str(self.education_background),
            "telephone": self.telephone,
            "email": self.email,
        })


class Project(models.Model):
    class Meta:
        db_table = "Project"
    year = models.IntegerField()
    major = models.CharField(max_length=56)
    birth_date = models.DateTimeField(default=timezone.now)

    contest = models.ForeignKey(to="contest.Contest", on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=128)
    name = models.CharField(max_length=128)
    student = models.ForeignKey(to="student.Student", on_delete=models.CASCADE)
    email = models.CharField(max_length=56)
    telephone = models.CharField(max_length=56)
    address = models.CharField(max_length=56)
    innovation = models.CharField(max_length=512)
    keywords = models.CharField(max_length=512)
    category = models.IntegerField()
    descriptions = models.CharField(max_length=2048)
    education_background = models.IntegerField()  # 0 1 2 3
    state = models.IntegerField()  # 0暂存中 1提交待初审 2初审过等待专家\\评审 3 专家评审过 等待确定答辩名单 4 进入答辩名单
    expire = models.IntegerField()  # 0可以访问可以操作（没过期） 1可以访问不能操作（已过期）

    type = models.IntegerField()  # 0 发明 创造 1 论文
    type_info = models.CharField(max_length=56)  # 类型信息

    def get_relate_cooperator(self):
        res = Cooperator.objects.filter(project=self)
        a = []
        for i in res:
            a.append(i.object2json())
        return a

    def object2json(self):
        return json.dumps({
            "type": str(self.type),
            "type_info": str(self.type_info),
            "year": self.year,
            "major": self.major,
            "full_name": self.full_name,
            "name": self.name,
            "student": self.student.student_id,
            "id": self.id,
            "birth_date": str(self.birth_date).split(" ")[0],
            "telephone": self.telephone,
            "address": self.address,
            "innovation": self.innovation,
            "keywords": self.keywords,
            "category": str(self.category),
            "descriptions": self.descriptions,
            "state": self.state,
            "cooperator": self.get_relate_cooperator(),
            "education_background": str(self.education_background),
            "email": self.email,
            "contest": self.contest.name if self.contest else "",
            "contest_id": self.contest.id if self.contest else -1
        })

    def admin_object2json(self):
        exps = Expert_projects.objects.filter(project_id=self.id)
        ret = {i.id: (i.expert_id, i.expert.name) for i in exps}
        return json.dumps({
            "type": str(self.type),
            "type_info": str(self.type_info),
            "year": self.year,
            "major": self.major,
            "full_name": self.full_name,
            "name": self.name,
            "student": self.student.student_id,
            "id": self.id,
            "birth_date": str(self.birth_date),
            "telephone": self.telephone,
            "address": self.address,
            "innovation": self.innovation,
            "keywords": self.keywords,
            "category": str(self.category),
            "descriptions": self.descriptions,
            "state": self.state,
            "cooperator": self.get_relate_cooperator(),
            "education_background": str(self.education_background),
            "email": self.email,
            "contest": self.contest.name if self.contest else "",
            "contest_id": self.contest.id if self.contest else -1,
            "expert_info": ret
        })

def project_not_exist(proj_id):
    if len(Project.objects.filter(id=proj_id)) < 1:
        return True
    else:
        return False


def project_expire(proj_id):
    return Project.objects.get(id=proj_id).expire == 1
