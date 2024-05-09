import imp
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, serializers
from rest_framework.decorators import action, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.exceptions import PermissionDenied
from .models import College, Student, Enrollment, Course, Teacher
from .serializers import  AddStudentSerializer, CollegeSerializer, SimpleCollegeSerializer, SimpleCourseSerializer, SimpleStudentSerializer, SimpleTeacherSerializer, StudentSerializer, EnrollmentSerializer, UpdateEnrollmentSerializer,CourseSerializer,TeacherSerializer, UpdateStudentSerializer, UpdateTeacherSerializer
from .filters import StudentFilter, TeacherFilter
from .permissions import StudentPermission, TeacherCanCreateCoursePermission, TeacherCanModifyProfilePermission, StudentCanModifyProfilePermission, TeacherAdminPermission, StudentCanChooseCoursePermission


 
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    filter_backends = [DjangoFilterBackend,SearchFilter]
    search_fields = ['user__username']
    filterset_class = StudentFilter

    
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method in ['PUT','PATCH']:
            return [StudentCanModifyProfilePermission()] 
        elif self.request.method in ['POST','DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ['PUT','PATCH']:
            return UpdateStudentSerializer
        elif self.request.method == 'POST':
            return StudentSerializer #其中发现创建用户时会需要选择identify_check 请设置为自动选择
        return SimpleStudentSerializer #这个里面的college展示需要优化

    @action(detail=False, methods=['GET', 'PUT'], url_path='me')
    def me(self, request):
        try:
            student = Student.objects.get(user_id=request.user.id)
        except Student.DoesNotExist:
            raise PermissionDenied("您没有资格访问.")
        
        if request.method == 'GET':
            serializer = StudentSerializer(student)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = StudentSerializer(student, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    filter_backends = [DjangoFilterBackend,SearchFilter]
    search_fields = ['user__username']
    filterset_class = TeacherFilter
    
    def get_serializer_class(self):
        if self.request.method in ['PUT','PATCH']:
            return UpdateTeacherSerializer
        elif self.request.method == 'POST':
            return TeacherSerializer
        return SimpleTeacherSerializer #这个里面的college展示需要优化

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT']:
            return [TeacherCanModifyProfilePermission()]
        elif self.request.method in ['POST','DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

    @action(detail=False, methods=['GET', 'PUT'],url_path='me')
    def me(self, request):
        try:
            teacher = Teacher.objects.get(user_id=request.user.id)
        except Teacher.DoesNotExist:
            raise PermissionDenied("您没有资格访问.")
        if request.method == 'GET':
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = TeacherSerializer(teacher, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class CourseViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend,SearchFilter]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    search_fields = ['name']


    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return [TeacherCanCreateCoursePermission()]

 

class TeacherCourseViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    ordering_fields = ['avg_score']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [TeacherCanCreateCoursePermission()]
        elif self.request.method == 'POST':
            return [TeacherCanCreateCoursePermission()]
        else:
            return [IsAdminUser()]


    def get_serializer_class(self):
        if self.request.method in ['PUT','PATCH']:
            return AddStudentSerializer
        else:
            return SimpleCourseSerializer

 
    def get_serializer_context(self):
        print(self.kwargs)
        if 'pk' not in self.kwargs:
            return {'teacher_id': self.kwargs['teacher_pk']}
        return {'teacher_id': self.kwargs['teacher_pk'], 'course_id': self.kwargs['pk']}

    def get_queryset(self):
        queryset = Course.objects.all()
        teacher_id = self.kwargs['teacher_pk']
        if teacher_id is not None:
            queryset=queryset.filter(teacher_id=teacher_id)
        return queryset

class EnrollmentViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.request.method in ['GET','POST']:
            return [StudentCanChooseCoursePermission()]
        else:
            return [TeacherAdminPermission()]
        

    #**************************#
    # 学生是否要根据grade选课？  #
    #**************************#
 

    # def perform_create(self, serializer):
    #     try:
    #         serializer.save()
    #     except serializers.ValidationError as e:
    #         return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


    def get_serializer_class(self):
        if self.request.method in ['PATCH','PUT']:
            return UpdateEnrollmentSerializer
        return EnrollmentSerializer

    def get_serializer_context(self):
        return {'student_id': self.kwargs['student_pk']}

    def get_queryset(self):
        return Enrollment.objects.filter(student_id=self.kwargs['student_pk'])
        

    


