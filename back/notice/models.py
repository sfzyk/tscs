import json
import time

from django.db import models
# Create your models here.


class Notice(models.Model):
    class Meta:
        db_table = "Notice"
    attach = models.FileField(upload_to='notice/', null=True)
    title=models.CharField(max_length=512)
    content=models.CharField(max_length=2048)
    time=models.DateTimeField()


    def object2json(self):
        return {
            "id": str(self.id),
            "title": str(self.title),
            "time": str(self.time).split(" ")[0]
        }
