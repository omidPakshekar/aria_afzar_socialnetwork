from rest_framework import permissions


class PostPermission(permissions.BasePermission):
    """
        every authenticate user can :create, 
        only admin can destory
        retreive, update : if you are admin or owner
        
    """ 
    def has_permission(self, request, view):
        print('view', view.action)

        if not request.user.is_authenticated:
            return False
        if view.action in ['list', 'add_like', 'add_user_saved']:
            return True
        elif view.action == 'mine':
            return True
        elif view.action in ['create', 'retrieve', 'update', 'partial_update', 'destroy']:
            return True
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        print('view', view.action)
        if not request.user.is_authenticated:
            return False
        if view.action in ['retrieve', 'add_like', 'add_user_saved']:
            return True
        elif view.action in [ 'update', 'partial_update']:
            return obj.owner == request.user or request.user.is_admin or request.user.is_staff
        elif view.action in ['destroy', 'change_status']:
            return request.user.is_admin or request.user.is_staff
        else:
            return False








