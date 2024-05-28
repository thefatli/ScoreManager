from urllib import response
from xml.dom.minidom import Identified
from django.db import transaction
from core.models import User
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from core.serializers import UserCreateSerializer, UserCreateSerializer2, UserSerializer
from .models import Student, Enrollment, Teacher,College,Course

class CollegeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = College
        fields = ['id', 'name', 'description']

class SimpleCollegeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = College
        fields = ['id', 'name']

class StudentCSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer2()
    college_name = serializers.SerializerMethodField()
    
    def get_college_name(self,obj):
        return obj.college.name if obj.college else None

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        college_name = validated_data.pop('college')
        user_data['identified_check'] = 'S'
        user = UserCreateSerializer2.create(UserCreateSerializer2(), validated_data=user_data)
        college, created = College.objects.get_or_create(name=college_name)
        student = Student.objects.create(user=user, college=college, **validated_data)
        
        return student

    class Meta:
        model = Student
        fields = ['id','user', 'gender', 'birth_date', 'info','grade', 'college_name','college']

class StudentSerializer(serializers.ModelSerializer):
    college_name = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.user.username 

    def get_email(self, obj):
        return obj.user.email 
    
    def get_college_name(self,obj):
        return obj.college.name if obj.college else None

    def create(self, validated_data):
        # 处理 college_name 字段
        college = validated_data.pop('college', None)
        if college:
            college_id = college.id
        else:
            # 设置默认学院
            college = College.objects.get_or_create(name='')[0]
            college_id = college.id
        # 创建 Student 实例
        student = Student.objects.create(college_id=college_id, **validated_data)
        return student

    class Meta:
        model = Student
        fields = ['id','name','user', 'gender', 'birth_date', 'info','email','grade', 'college_name','college']

    def calculate_score(self, student: Student):
        return sum([course for course in student.courses.all()])

class SimpleStudentSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    college = CollegeSerializer()
    def get_email(self, obj):
        return obj.user.email 
    class Meta:
        model = Student
        fields = ['id', 'name', 'gender', 'college', 'grade','email']

class TeacherCSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer2()
    college_name = serializers.SerializerMethodField()
    
    def get_college_name(self,obj):
        return obj.college.name if obj.college else None

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        college_name = validated_data.pop('college')
        user_data['identified_check'] = 'S'
        user = UserCreateSerializer2.create(UserCreateSerializer2(), validated_data=user_data)
        college, created = College.objects.get_or_create(name=college_name)
        teacher = Teacher.objects.create(user=user, college=college, **validated_data)
        return teacher

    class Meta:
        model = Teacher
        fields = ['id','user', 'gender', 'birth_date', 'info', 'college_name','college']

class TeacherSerializer(serializers.ModelSerializer):
    # user = UserCreateSerializer()
    college_name = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_name(self, obj):
        return obj.user.username 

    def get_email(self, obj):
        return obj.user.email 
    
    def get_college_name(self,obj):
        return obj.college.name if obj.college else None
    
    def create(self, validated_data):
        college = validated_data.pop('college', None)
        if college:
            college_id = college.id
        else:
            # 设置默认学院
            college = College.objects.get_or_create(name='')[0]
            college_id = college.id
        teacher = Teacher.objects.create(college_id=college_id, **validated_data)
        return teacher

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'gender', 'birth_date', 'info','college_name','college','name', 'email']

class SimpleTeacherSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    def get_email(self, obj):
        return obj.user.email 
    college = CollegeSerializer()
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'gender', 'college','email']
 

class EnrollmentSerializer(serializers.ModelSerializer):
    course_name = serializers.SerializerMethodField()
    student_name = serializers.SerializerMethodField()

    def get_course_name(self, obj):
            return obj.course.name if obj.course else None
    def get_student_name(self, obj):
        return obj.student.user.username if obj.student else None
            
    class Meta:
        model = Enrollment
        fields = ['id', 'course_name', 'course', 'score','student_name','student']
        read_only_fields = ['course_name','score','student_name','student']

    
    def validate_course_id(self, value):
        if not Course.objects.filter(pk=value).exists():
            raise serializers.ValidationError('该课程不存在.')
        return value

    def create(self, validated_data):
        student_id = self.context.get('student_id')
        course_id = validated_data.get('course').id
        if Enrollment.objects.filter(student_id=student_id, course_id=course_id).exists():
            raise serializers.ValidationError('该课程已经添加.')
        enrollment = Enrollment.objects.create(student_id=student_id, course_id=course_id, **validated_data)
        enrollment.save() 
        return enrollment


class CourseSerializer(serializers.ModelSerializer):
    items = EnrollmentSerializer(many=True, read_only=True)
    avg_score = serializers.SerializerMethodField()
    college_name = serializers.SerializerMethodField()
    teacher_name = serializers.SerializerMethodField()

    def get_teacher_name(self, obj):
            return obj.teacher.user.username if obj.teacher else None

    def get_college_name(self, obj):
            return obj.college.name if obj.college else None


    def get_avg_score(self, course):
        total_score = sum(item.score for item in course.items.all() if item.score is not None)
        total_items = course.items.exclude(score=None).count()
        if total_items > 0:
            return total_score / total_items
        else:
            return None

    class Meta:
        model = Course
        fields = ['id', 'grade', 'name', 'college', 'college_name', 'teacher', 'point', 'items', 'avg_score','time','teacher_name']
        read_only_fields = ['items', 'avg_score']


class SimpleCourseSerializer(serializers.ModelSerializer):
    items = EnrollmentSerializer(many=True, read_only=True)
    avg_score = serializers.SerializerMethodField()

    def create(self, validated_data):
        teacher_id = self.context['teacher_id']
        name = validated_data['name']
        grade = validated_data['grade']
        college = validated_data.pop('college', None)
        # print(validated_data)
        if college:
            college_id = college.id
            # print(college)
        else:
            # 设置默认学院
            # print(college)
            college = College.objects.get_or_create(name='')[0]
            college_id = college.id
        if Course.objects.filter(teacher_id=teacher_id, name=name, grade=grade).exists():
            raise serializers.ValidationError('该课程已经添加.')
        return Course.objects.create(teacher_id=teacher_id, college_id=college_id, **validated_data)

    def get_avg_score(self, course):
        total_score = sum(item.score for item in course.items.all() if item.score is not None)
        total_items = course.items.exclude(score=None).count()
        if total_items > 0:
            return total_score / total_items
        else:
            return None

    class Meta:
        model = Course
        fields = ['id','grade', 'name', 'point', 'items', 'avg_score', 'college']
        read_only_fields = ['items', 'avg_score']


class AddStudentSerializer(serializers.ModelSerializer):
    students = serializers.ListSerializer(child=serializers.PrimaryKeyRelatedField(queryset=Student.objects.all()), allow_empty=False)
    def save(self, **kwargs):
        with transaction.atomic():
            course_id = self.context['course_id']
            # 获取学生数据列表
            students_data = self.validated_data.get('students')
            for student in students_data:
                student_id = student.id      
                # 检查是否已经添加过该学员
                if Enrollment.objects.filter(student_id=student_id, course_id=course_id).exists():
                    raise serializers.ValidationError(f'学员 {student_id} 已经添加.')            
                # 创建 Enrollment 对象
                enrollment = Enrollment.objects.create(course_id=course_id, student_id=student_id)
                # 将 enrollment 添加到 course 的 items 中
                course = enrollment.course
        return course

    class Meta:
        model = Course
        fields = ['id', 'students']


class UpdateEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = ['score']


class UpdateStudentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email',allow_blank=True, required=False)
    name = serializers.CharField(source='user.username') 

    class Meta:
        model = Student
        fields = ['name', 'college', 'gender', 'email', 'grade','info','birth_date']
        read_only_fields = ['name']


    def update(self, instance, validated_data):
        # 获取 user 数据
        user_data = validated_data.pop('user', None)
        # 更新 user 数据
        if user_data:
            if 'email' in user_data:
                instance.user.email = user_data['email']
            if 'username' in user_data:
                instance.user.username = user_data['username']
            instance.user.save()
        # 更新 Student 数据
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UpdateTeacherSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email',allow_blank=True, required=False)
    name = serializers.CharField(source='user.username') 

    class Meta:
        model = Teacher
        fields = ['name', 'college', 'gender', 'email']

    def update(self, instance, validated_data):
        # 获取 user 数据
        user_data = validated_data.pop('user', None)
        # 更新 user 数据
        if user_data:
            if 'email' in user_data:
                instance.user.email = user_data['email']
            if 'username' in user_data:
                instance.user.username = user_data['username']
            instance.user.save()
        # 更新 Teacher 数据
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance









