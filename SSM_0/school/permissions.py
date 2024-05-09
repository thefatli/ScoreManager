from rest_framework import permissions

# 优化permission
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
            if request.user.identified_check == 'T':
                if obj.user == request.user:
                    return True
        return False

class StudentCanModifyProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):#适用于用户对单个对象的操作，故List不受操控
        if request.user.is_authenticated:
            if request.user.identified_check == 'S':
                return obj.user == request.user
        return False

class StudentCanChooseCoursePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # 检查是否经过身份验证
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        # 检查用户是否有关联的学生
        if not hasattr(request.user, 'student'):
            return False
        # 检查是否是学生本人
        student_pk = view.kwargs.get('student_pk')
        return str(request.user.student.pk) == student_pk


class TeacherCanCreateCoursePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        # 检查是否经过身份验证
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if not hasattr(request.user, 'teacher'):
            return False
        # 检查是否是本人
        teacher_pk = view.kwargs.get('teacher_pk')
        return str(request.user.teacher.pk) == teacher_pk



 
