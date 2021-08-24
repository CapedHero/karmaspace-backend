from typing import Protocol

from django.views import View
from rest_framework import permissions
from rest_framework.request import Request

from src.app_auth.models import User


class HasOwner(Protocol):
    owner: User


class IsAccessingOwnResourceOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return request.user.username == view.kwargs.get("username")


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: HasOwner) -> bool:
        return obj.owner == request.user
