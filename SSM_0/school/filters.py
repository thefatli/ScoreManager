from django_filters import FilterSet
from .models import Student, Teacher

class StudentFilter(FilterSet):
    class Meta:
        model = Student
        fields = {
            'gender': ['exact'],
            'college': ['exact'],
            'birth_date': ['year__gt', 'year__lt'],
        }

class TeacherFilter(FilterSet):
    class Meta:
        model = Teacher
        fields = {
            'gender': ['exact'],
            'college': ['exact'],
            'birth_date': ['year__gt', 'year__lt'],
        }

