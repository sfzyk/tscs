from django.db import models
import json

class Expert_projects(models.Model):
    class Meta:
        db_table = "Expert_Projects"
    project = models.ForeignKey(to='project.Project', on_delete=models.CASCADE)
    expert = models.ForeignKey(to='Expert', on_delete=models.CASCADE)
    contest = models.ForeignKey(to="contest.Contest", on_delete=models.CASCADE)


class Expert_contests(models.Model):
    class Meta:
        db_table = "Expert_Contests"
    expert = models.ForeignKey(to="Expert", on_delete=models.CASCADE)
    contest = models.ForeignKey(to="contest.Contest", on_delete=models.CASCADE)
    state = models.IntegerField()#0发出邀请  1接收邀请  2拒绝邀请
    session = models.CharField(max_length=56)

class Expert(models.Model):
    class Meta:
        db_table = "Expert"
    name = models.CharField(max_length=128, null="True")  # 姓名
    email = models.CharField(max_length=32, unique=True)  # 邮箱
    password = models.CharField(max_length=64)  # 密码
    field = models.IntegerField()  # 领域
    state = models.IntegerField()  # 状态 0 没状态 1 有状态
    telephone = models.CharField(max_length=32, null=True)  # 联系电话
    college = models.CharField(max_length=32, null=True)

    def object2json(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "email":  self.email,
            "field": self.field,
            "state": self.state,
            "telephone": self.telephone,
            "college": self.college
        })

    def objectcontest2json(self):
        con = Expert_contests.objects.filter(expert_id=self.id)
        contest_state = 0 if con.count() == 0 else con[0].state + 1
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "email":  self.email,
            "field": self.field,
            "state": self.state,
            "telephone": self.telephone,
            "college": self.college,
            'contest_state': contest_state
        })


def duplicate_email(e):
    return len(Expert.objects.filter(email=e)) > 0