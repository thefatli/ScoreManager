from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('', views.UserProfileViewSet, basename='profile')
router.register('students', views.StudentViewSet, basename='students')
router.register('teachers', views.TeacherViewSet, basename='teachers')
router.register('courses', views.CourseViewSet, basename='courses')
router.register('colleges', views.CollegeViewSet, basename='colleges')  # 注意这里的 basename='colleges'



students_router = routers.NestedDefaultRouter(router, 'students', lookup='student')
students_router.register('courses', views.EnrollmentViewSet,basename='students-enrollment')

teachers_router = routers.NestedDefaultRouter(router, 'teachers', lookup='teacher')
teachers_router.register('courses', views.TeacherCourseViewSet, basename='teachers-courses')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(students_router.urls)),
    path('', include(teachers_router.urls)),
    path('students/post', views.StudentCreateView.as_view(), name='student-post'),
    path('teachers/post', views.TeacherCreateView.as_view(), name='teacher-post'),
    path('collegelist/', views.CollegeListView.as_view(), name='college-list'),
    path('teacherlist/', views.TeacherListView.as_view(), name='teacher-list'),
    path('studentlist/', views.StudentListView.as_view(), name='student-list'),

]


