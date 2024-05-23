from django.contrib import admin
from .models import College,Student,Teacher,Course,Enrollment
from django import forms


# Register your models here.
#学院表
class CollegeAdmin(admin.ModelAdmin):
    #列表页显示学院名和学院介绍
    list_display = ['name','description']
    #添加输入学院名搜索
    search_fields = ['name']
admin.site.register(College,CollegeAdmin)

#学生表
class StudentAdmin(admin.ModelAdmin):
    # 定义列表页从左到右显示学号，姓名，学院
    list_display = ('student_id', 'name', 'college')
    # 定义点击学号或姓名可编辑
    list_display_links = ('student_id', 'name')
    # 设置表按学号升序排序
    ordering = ('id',)
    # 设置编辑页从上到下显示姓名，性别，出生日期，年级，所属学院，其他
    fields = ['user', 'gender', 'birth_date', 'grade', 'college','info']
    #按年级，学院，性别分类
    list_filter = ['college','grade','gender']
    #按学生名字搜索
    search_fields = ['user__username']
    def student_id(self, obj):
        return obj.pk
    student_id.short_description = '学号'
    def name(self,obj):
        return obj.user.username
    name.short_description = '姓名'

admin.site.register(Student, StudentAdmin)

#老师
class TeacherAdmin(admin.ModelAdmin):
    #显示姓名，学院
    list_display = ['name','college']
    #设置编辑页字段顺序
    fields = ['user','gender','birth_date','college','info']
    #搜索
    search_fields = ['user__username']
    #分类
    list_filter = ['college','gender']
    def name(self,obj):
        return obj.user.username
    name.short_description = "姓名"
admin.site.register(Teacher,TeacherAdmin)

#课程
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name','point','grade','college','teacher']
    list_filter = ['grade','college','teacher']
    search_fields = ['name']

admin.site.register(Course,CourseAdmin)
#
#学生-课程
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student','course','score']
    #点击学生名或课程名编辑
    list_display_links = ['student','course']
    #按学生或课程搜索
    search_fields = ['student__user__username','course__name']

admin.site.register(Enrollment,EnrollmentAdmin)


