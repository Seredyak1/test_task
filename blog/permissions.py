from rest_framework import permissions


class IsPostOwner(permissions.BasePermission):
    """
    Object-level permission to only allow updating his own profile
    PUT and DELETE methods just for the user, who is owner of Post
    """
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user
