from rest_framework.permissions import BasePermission, SAFE_METHODS
class PublicReadStaffWrite(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or bool(request.user and request.user.is_staff)
