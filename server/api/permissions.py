from rest_framework.permissions import SAFE_METHODS, BasePermission


class ReadOnly(BasePermission):
    """GET OPTIONS HEAD のリクエストのみを通す権限
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
