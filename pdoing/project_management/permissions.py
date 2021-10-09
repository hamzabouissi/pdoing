from rest_framework import permissions

from pdoing.users.models import UserTypeEnum


class TaskCreatorPermission(permissions.BasePermission):
    # message = " Your not owner of task"

    def has_object_permission(self, request, view, obj):
        return obj.task.author == request.user


class DeveloperTaskOwnerPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.developer == request.user


#
# class IsInstructorPermission(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         return request.user.user_type == UserTypeEnum.Instructor

# class CanAddTaskPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         if request.method == "POST" and request.user.is_authenticated:
#             message = "You must Be authenticated Instructor"
#             return request.user.user_type == UserTypeEnum.Instructor
#         return True


class IsInstructorPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST" and request.user.is_authenticated:
            message = "You must Be authenticated Instructor"
            return request.user.user_type == UserTypeEnum.Instructor
        return True
