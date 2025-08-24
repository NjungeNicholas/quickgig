from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Others can only read it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions are only allowed to the owner of the object
        return obj == request.user


class IsTaskerOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission for tasker profiles.
    Only the owner can edit their profile, others can read if authenticated.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        # Write permissions are only allowed to the owner of the tasker profile
        return obj.user == request.user


class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        # All permissions are only allowed to the owner of the object
        return obj == request.user


class IsTaskerOwner(permissions.BasePermission):
    """
    Custom permission for tasker profiles.
    Only the owner can access their profile.
    """

    def has_object_permission(self, request, view, obj):
        # All permissions are only allowed to the owner of the tasker profile
        return obj.user == request.user


class IsAuthenticatedOrCreateOnly(permissions.BasePermission):
    """
    Custom permission to allow unauthenticated users to create accounts,
    but require authentication for other operations.
    """

    def has_permission(self, request, view):
        # Allow POST (create) for unauthenticated users
        if request.method == 'POST' and view.action == 'create':
            return True
        
        # For all other operations, require authentication
        return request.user.is_authenticated


class IsTasker(permissions.BasePermission):
    """
    Custom permission to only allow taskers.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_tasker


class IsClient(permissions.BasePermission):
    """
    Custom permission to only allow clients.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_client


class IsTaskerOrClient(permissions.BasePermission):
    """
    Custom permission to allow both taskers and clients.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_tasker or request.user.is_client
        )