from cgitb import lookup
from django.urls import path
from django.urls.conf import include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('students', views.StudentViewSet, basename='students')
router.register('teachers', views.TeacherViewSet, basename='teachers')
router.register('courses', views.CourseViewSet, basename='courses')

# 过于冗杂 
students_router = routers.NestedDefaultRouter(router, 'students', lookup='student')
students_router.register('courses', views.EnrollmentViewSet,basename='students-enrollment')

teachers_router = routers.NestedDefaultRouter(router, 'teachers', lookup='teacher')
teachers_router.register('courses', views.TeacherCourseViewSet, basename='teachers-courses')

# URLConf
urlpatterns = router.urls + students_router.urls + teachers_router.urls
