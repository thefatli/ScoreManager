from urllib import response
from django.db import transaction
from core.models import User
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from core.serializers import UserCreateSerializer
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

# # 首先得创建College，才可以创建Grade
# class GradeSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     college = CollegeSerializer()

#     def create(self, validated_data):
#         college_data = validated_data.pop('college')
#         college, _ = College.objects.get_or_create(**college_data)
#         validated_data['college'] = college
#         return Grade.objects.create(validated_data)

#     class Meta:
#         model = Grade
#         fields = ['id', 'name','college']


class StudentSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        college_id = College.objects.get(name=validated_data['college']).id
        user = User.objects.create(**user_data)
        student, created = Student.objects.get_or_create(user=user, college_id=college_id, **validated_data)
        student.save()
        return student

    class Meta:
        model = Student
        fields = ['id', 'user', 'gender', 'birth_date', 'info', 'grade', 'college']

    def calculate_score(self, student: Student):
        return sum([course for course in student.courses.all()])

class SimpleStudentSerializer(serializers.ModelSerializer):
    college = CollegeSerializer()
    class Meta:
        model = Student
        fields = ['name', 'gender', 'college', 'grade']

class TeacherSerializer(serializers.ModelSerializer):
    user = UserCreateSerializer()
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        college_id = College.objects.get(name=validated_data['college']).id
        user = User.objects.create(**user_data)
        teacher, created = Teacher.objects.get_or_create(user=user, college_id=college_id, **validated_data)
        teacher.save()
        return teacher

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'gender', 'birth_date', 'info','college']

class SimpleTeacherSerializer(serializers.ModelSerializer):
    college = CollegeSerializer()
    class Meta:
        model = Teacher
        fields = ['name', 'gender', 'college']
 

class EnrollmentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Enrollment
        fields = ['id', 'course']
    
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

    def get_avg_score(self, course):
        total_score = sum(item.score for item in course.items.all() if item.score is not None)
        total_items = course.items.exclude(score=None).count()
        if total_items > 0:
            return total_score / total_items
        else:
            return None

    class Meta:
        model = Course
        fields = ['id', 'grade', 'name', 'teacher', 'point', 'items', 'avg_score']
        read_only_fields = ['items', 'avg_score']


class SimpleCourseSerializer(serializers.ModelSerializer):
    items = EnrollmentSerializer(many=True, read_only=True)
    avg_score = serializers.SerializerMethodField()

    def create(self, validated_data):
        teacher_id = self.context['teacher_id']
        name = validated_data['name']
        grade = validated_data['grade']
        if Course.objects.filter(teacher_id=teacher_id, name=name, grade=grade).exists():
            raise serializers.ValidationError('该课程已经添加.')
        return Course.objects.create(teacher_id=teacher_id, **validated_data)

    def get_avg_score(self, course):
        total_score = sum(item.score for item in course.items.all() if item.score is not None)
        total_items = course.items.exclude(score=None).count()
        if total_items > 0:
            return total_score / total_items
        else:
            return None

    class Meta:
        model = Course
        fields = ['id','grade', 'name', 'point', 'items', 'avg_score']
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
    class Meta:
        model = Student
        fields = ['info']

class UpdateTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['info']









