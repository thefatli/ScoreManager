from tkinter.tix import Tree
from rest_framework import permissions

class TeacherAdminPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:  
            if request.user.identified_check == 'T' or request.user.is_staff:
                return True
        return False

class StudentPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated: 
            if request.user.identified_check == 'S':
                return True
        return False


class TeacherCanModifyProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            if request.user.identified_check == 'T':
                if obj.user == request.user:
                    return True
        return False

class StudentCanModifyProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return True
            if request.user.identified_check == 'S':
                return obj.user == request.user
        return False

class StudentCanChooseCoursePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if  hasattr(request.user, 'teacher'):
            return True
        if not hasattr(request.user, 'student'):
            return False
 
        student_pk = view.kwargs.get('student_pk')
        return str(request.user.student.pk) == student_pk


class TeacherCanCreateCoursePermission(permissions.BasePermission):
    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if not hasattr(request.user, 'teacher'):
            return False
 
        teacher_pk = view.kwargs.get('teacher_pk')
        return str(request.user.teacher.pk) == teacher_pk



 
