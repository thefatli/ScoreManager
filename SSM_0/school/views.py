from rest_framework import viewsets, generics
from rest_framework import status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.exceptions import PermissionDenied
from core.serializers import UserSerializer
from .models import College, Student, Teacher, Course, Enrollment
from .serializers import (
    CollegeSerializer, StudentCSerializer, StudentSerializer, TeacherCSerializer, UpdateStudentSerializer, SimpleStudentSerializer,
    TeacherSerializer, UpdateTeacherSerializer, SimpleTeacherSerializer,
    CourseSerializer, AddStudentSerializer, SimpleCourseSerializer,
    EnrollmentSerializer, UpdateEnrollmentSerializer
)
from .permissions import (
    StudentCanModifyProfilePermission, TeacherCanModifyProfilePermission,
    TeacherCanCreateCoursePermission, StudentCanChooseCoursePermission, TeacherAdminPermission
)
from .pagination import DefaultPagination
from .filters import StudentFilter, TeacherFilter

class CollegeListView(generics.ListAPIView):
    queryset = College.objects.exclude(id=4)
    serializer_class = CollegeSerializer

    def get_queryset(self):
        # Disable pagination for this view
        self.pagination_class = None
        return super().get_queryset()

class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        # Disable pagination for this view
        self.pagination_class = None
        return super().get_queryset()

class TeacherListView(generics.ListAPIView):
    queryset = Teacher.objects.all()
    serializer_class = StudentSerializer

    def get_queryset(self):
        # Disable pagination for this view
        self.pagination_class = None
        return super().get_queryset()


class CollegeViewSet(viewsets.ModelViewSet):
    queryset = College.objects.exclude(id=4)

    serializer_class = CollegeSerializer
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['name']


class UserProfileViewSet(viewsets.ViewSet):

    def get_permissions(self):
        if self.action in ['me']:
            return [IsAuthenticated()]
        return [AllowAny()]

    @action(detail=False, methods=['GET'], url_path='identified_check')
    def identified_check(self, request):
        user = request.user
        return Response({'identified_check': user.identified_check})

    @action(detail=False, methods=['GET', 'PUT'], url_path='me')
    def me(self, request):
        user = request.user
        
        if hasattr(user, 'student'):
            profile = user.student
            read_serializer_class = StudentSerializer
            update_serializer_class = UpdateStudentSerializer
        elif hasattr(user, 'teacher'):
            profile = user.teacher
            read_serializer_class = TeacherSerializer
            update_serializer_class = UpdateTeacherSerializer
        else:
            profile = user
            read_serializer_class = UserSerializer
            update_serializer_class = None
        
        if request.method == 'GET':
            serializer = read_serializer_class(profile)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            if update_serializer_class is None:
                raise PermissionDenied("您没有资格修改此信息.")
            
            serializer = update_serializer_class(profile, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class StudentCreateView(CreateModelMixin, GenericAPIView):
    serializer_class = StudentCSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class TeacherCreateView(CreateModelMixin, GenericAPIView):
    
    serializer_class = TeacherCSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class StudentViewSet(viewsets.ModelViewSet):
    pagination_class = DefaultPagination
    queryset = Student.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__username','college__name']
    filterset_class = StudentFilter

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        if self.request.method in ['PUT', 'PATCH']:
            return [StudentCanModifyProfilePermission()] 
        elif self.request.method in [ 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateStudentSerializer
        elif self.request.method == 'POST':
            return StudentSerializer
        return SimpleStudentSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    pagination_class = DefaultPagination
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['user__username','college__name']
    filterset_class = TeacherFilter

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateTeacherSerializer
        elif self.request.method == 'POST':
            return TeacherSerializer
        return SimpleTeacherSerializer

    def get_permissions(self):
        if self.request.method in ['PATCH', 'PUT']:
            return [TeacherCanModifyProfilePermission()]
        elif self.request.method in ['POST', 'DELETE']:
            return [IsAdminUser()]
        return [AllowAny()]

class CourseViewSet(viewsets.ModelViewSet):
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    search_fields = ['name','college__name','teacher__user__username']

    # def get_permissions(self):
    #     if self.request.method == 'GET':
    #         return [AllowAny()]
    #     return [TeacherCanCreateCoursePermission()]

class TeacherCourseViewSet(viewsets.ModelViewSet):
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    #filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['avg_score']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method in ['DELETE', 'PUT', 'PATCH']:
            return [TeacherCanCreateCoursePermission()]
        elif self.request.method == 'POST':
            return [TeacherCanCreateCoursePermission()]
        return [IsAdminUser()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AddStudentSerializer
        return SimpleCourseSerializer

    def get_serializer_context(self):
        if 'pk' not in self.kwargs:
            return {'teacher_id': self.kwargs['teacher_pk']}
        return {'teacher_id': self.kwargs['teacher_pk'], 'course_id': self.kwargs['pk']}

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Course.objects.none()
        queryset = Course.objects.all()
        teacher_id = self.kwargs.get('teacher_pk')
        if teacher_id is not None:
            queryset = queryset.filter(teacher_id=teacher_id)
        return queryset

class EnrollmentViewSet(viewsets.ModelViewSet):
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['course__name']
    def get_permissions(self):
        return [StudentCanChooseCoursePermission()]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return UpdateEnrollmentSerializer
        return EnrollmentSerializer

    def get_serializer_context(self):
        return {'student_id': self.kwargs.get('student_pk')}

    def get_queryset(self):
        student_id = self.kwargs.get('student_pk')
        if student_id is not None:
            return Enrollment.objects.filter(student_id=student_id)
        return Enrollment.objects.none()
