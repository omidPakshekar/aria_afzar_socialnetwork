from rest_framework import permissions

class UserViewSetPermission(permissions.BasePermission):
    """
        every authenticate user can : get 
        only admin can destory, create,
    """ 
    def has_permission(self, request, view):
        print('view', view.action)

        if not request.user.is_authenticated:
            return False
        if view.action in ['list', 'mine']:
            return True
        elif view.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if view.action in ['retrieve', 'add_like', 'add_user_saved', 'add_comment']:
            return True
        elif view.action in [ 'update', 'partial_update']:
            return obj.owner == request.user or request.user.is_admin or request.user.is_staff
        elif view.action in ['destroy', 'change_status']:
            return request.user.is_admin or request.user.is_staff
        else:
            return False






