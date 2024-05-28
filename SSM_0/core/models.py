
from django.contrib.auth.models import AbstractUser
from django.db import models
from .validators import validate_file_size

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
    username = models.CharField(
        verbose_name="用户名称",
        max_length=100,
        unique=True
        )
    identified_check = models.CharField(
        max_length=1, 
        choices=IDENTIFICATION_CHOICES, 
        default=STUDENT
        )
    image = models.ImageField(
        upload_to='core/images', 
        validators=[validate_file_size],
        default='core/images/default.png'
        )

    