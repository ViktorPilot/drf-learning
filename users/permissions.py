from rest_framework import permissions


class IsModerators(permissions.BasePermission):

    def has_permission(self, request, view):
        """Метод проверяет находится ли пользователь в группе модераторов"""
        return request.user.groups.filter(name="moderators").exists()

    def has_object_permission(self, request, view, obj):
        """Метод проверяет находится ли пользователь в группе модераторов"""
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """Метод проверяет является ли пользователь владельцем"""
        return obj.owner == request.user
