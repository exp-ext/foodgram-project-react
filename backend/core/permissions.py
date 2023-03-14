from django.db.models import Model
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class IsAdmin(BasePermission):
    """
    Права доступа: Администратор.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return request.user.is_authenticated and request.user.is_admin

    def has_object_permission(self,
                              request: Request,
                              view: View,
                              obj: Model) -> bool:
        return request.user.is_authenticated and request.user.is_admin


class ReadOnly(BasePermission):
    """
    Права доступа: Чтение.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return request.method in SAFE_METHODS

    def has_object_permission(self,
                              request: Request,
                              view: View,
                              obj: Model) -> bool:
        return request.method in SAFE_METHODS


class IsOwner(BasePermission):
    """
    Права доступа: Автор.
    """

    def has_permission(self, request: Request, view: View) -> bool:
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_active
        )

    def has_object_permission(self,
                              request: Request,
                              view: View,
                              obj: Model) -> bool:
        return request.user and request.user == obj.author
