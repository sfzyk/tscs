from django.db import models
import re


class Student(models.Model):
    class Meta:
        db_table = "Student"
    student_id = models.CharField(max_length=32)
    password = models.CharField(max_length=32)  # 密码
    name = models.CharField(max_length=128, null=True)  # 姓名
    department = models.CharField(max_length=128, null=True)  # 部门
    email = models.CharField(max_length=128, unique=True)  # 邮箱
    major = models.CharField(max_length=128, null=True)  # 专业
    year = models.IntegerField(null=True)  # 入学年份
    telephone = models.CharField(max_length=128, null=True)  # 联系电话
    birth_date = models.DateTimeField(max_length=128)


