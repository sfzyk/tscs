from django.db import models
import json


class Contest(models.Model):
    class Meta:
        db_table = "Contest"
    name = models.CharField(max_length=56)
    descriptions = models.CharField(max_length=4096)
    expire_date = models.DateTimeField()
    checkin_expire_date = models.DateTimeField()
    state = models.IntegerField()  # 0审核中  # 1报名  # 2初审  # 2初评  # 3筛选出答辩名单 # 4最终结果

    def object2json(self):
        return json.dumps({
            "id": self.id,
            "name": self.name,
            "descriptions": self.descriptions,
            "expire_date": str(self.expire_date),
            "checkin_expire_date": str(self.checkin_expire_date),
            "state": self.state
        })


class FinalStage(models.Model):
    class Meta:
        db_table = "FinalSatge"
    contest = models.ForeignKey(to="contest.Contest", on_delete=models.CASCADE)
    result = models.CharField(max_length=6000)
