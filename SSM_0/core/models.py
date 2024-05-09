
from django.contrib.auth.models import AbstractUser
from django.db import models

STUDENT = 'S'
Administrator = 'A'
TEACHER = 'T'
IDENTIFICATION_CHOICES = [
    (STUDENT, '学生'),
    (Administrator, '管理员'),
    (TEACHER, '教师')
]

# Create your models here.
class User(AbstractUser):
    id = models.CharField( primary_key=True, max_length=8, verbose_name="学号")
    username = models.CharField(verbose_name="用户名称",max_length=100,unique=True)
    identified_check = models.CharField(max_length=1, choices=IDENTIFICATION_CHOICES, default=STUDENT)
    