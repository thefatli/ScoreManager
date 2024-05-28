from turtle import title
from django.db import models
from django.contrib import admin
from django.conf import settings

GENDER_MALE = '男'
GENDER_FEMALE = '女'
GENDER_CHOICES = [
    (GENDER_MALE, '男'),
    (GENDER_FEMALE, '女'),
]

GRADE_ONE = '1'
GRADE_TWO = '2'
GRADE_THREE = '3'
GRADE_FOUR = '4'
GRADE_CHOICES = [
    (GRADE_ONE, '大一'),
    (GRADE_TWO, '大二'),
    (GRADE_THREE, '大三'),
    (GRADE_FOUR, '大四'),
]

# Create your models here.
class College(models.Model):
    name = models.CharField(verbose_name="学院名称",max_length=100,unique=True, blank=True,null=True)
    description = models.TextField() 

    def __str__(self):
        return self.name


class Student(models.Model):
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES,default=GRADE_ONE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,default='女')
    birth_date = models.DateField(null=True, blank=True)
    info = models.CharField(max_length=200,blank=True,null=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE, blank=True, null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        # 先删除User实例
        self.user.delete()
        # 然后删除Student实例
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.user.username

    @admin.display(ordering='user__username')
    def name(self):
        return self.user.username
    
    class Meta:
        ordering = ['user__username']


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='女')
    birth_date = models.DateField(null=True, blank=True)
    info = models.CharField(max_length=200,blank=True,null=True)
    college = models.ForeignKey(College,on_delete=models.PROTECT,related_name="teachers", blank=True, null=True)

    def delete(self, *args, **kwargs):
        # 先删除User实例
        self.user.delete()
        # 然后删除Student实例
        super().delete(*args, **kwargs)

    @admin.display(ordering='user__username')
    def name(self):
        return self.user.username
    
    def __str__(self):
        return self.user.username
        
    class Meta:
        ordering = ['user__username']

class Course(models.Model):
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES)
    college = models.ForeignKey(College, verbose_name="所属学院", related_name='courses', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    point = models.FloatField(verbose_name="学分",null=False)
    students = models.ManyToManyField(Student, verbose_name="学生姓名", related_name='courses', through='Enrollment')
    teacher = models.ForeignKey(Teacher, verbose_name="教师姓名", on_delete=models.CASCADE)
    time = models.PositiveIntegerField(verbose_name="课时",null=False, default=0)


    def __str__(self):
        return self.name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE,related_name='items')
    score = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, default=None)

    class Meta:
        unique_together = [['student', 'course']]

    def __str__(self):
        return f"{self.student} - {self.course}"

