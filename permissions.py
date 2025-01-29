from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    message = "Not allowed to perform this action"
    def has_permission(self, request, view):
        return request.user.role == "admin"
