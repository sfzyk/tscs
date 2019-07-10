from django.db import models
import json
# Create your models here.


class Comment(models.Model):
    class Meta:
        db_table = "Comment"
        unique_together = ("expert", "project")
    comment = models.CharField(max_length=3000)
    score = models.FloatField()
    expert = models.ForeignKey(to="expert.Expert",on_delete=models.CASCADE)
    project = models.ForeignKey(to="project.Project",on_delete=models.CASCADE)
    state = models.IntegerField() # 0 暂存中， 1 确认
    def object2json(self):
        return json.dumps(
            {
                "comment":self.comment,
                "score":self.score,
                "expert_name":self.expert.name,
            }
        )