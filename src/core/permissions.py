from django.views import View
from rest_framework import permissions
from rest_framework.request import Request


class IsAccessingOwnResourceOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.username == view.kwargs.get("username")
