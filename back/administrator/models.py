from django.db import models
# Create your model here.


class Administrator(models.Model):
    class Meta:
        db_table = "Administrator"

    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=64)


class Config(models.Model):
    class Meta:
        db_table = "Config"
    expert_per_proj = models.IntegerField() # 0 not 1 do auto dispath
    num_proj = models.IntegerField()