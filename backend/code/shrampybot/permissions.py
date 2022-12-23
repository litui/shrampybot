# Pattern copied unabashedly from DRF

class BasePermission():

    def has_permission(self):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True

    def has_object_permission(self, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        return True


class AllowAny(BasePermission):

    def has_permission(self):
        return True


class IsAuthenticated(BasePermission):

    def has_permission(self):
        return bool(self.scope.get('user') and self.scope['user'].is_authenticated)


class IsAdminUser(BasePermission):

    def has_permission(self):
        return bool(self.scope.get('user') and self.scope['user'].is_staff)


