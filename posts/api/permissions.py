from rest_framework import permissions


class PostPermission(permissions.BasePermission):
    """
        every authenticate user can :create, 
        only admin can destory
        retreive, update : if you are admin or owner
        
    """ 
    def has_permission(self, request, view):
        print('view', view.action)
        if view.action in ['list', 'retrieve']:
            return True
        if not request.user.is_authenticated:
            return False
        if view.action in ['get_comment', 'add_like', 'add_user_saved', 'admin_accept' ,'add_comment', 'mine']:
            return True
        elif view.action in ['create', 'retrieve', 'partial_update', 'destroy', 'update']:
            return True
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve']:
            return True
        if not request.user.is_authenticated:
            return False
        if view.action in ['get_comment', 'add_like', 'add_user_saved' ,'add_comment']:
            return True
        elif view.action in [ 'update', 'partial_update']:
            return obj.owner == request.user or request.user.is_admin or request.user.is_staff
        elif view.action in ['destroy', 'change_status', 'admin_accept']:
            return request.user.is_admin or request.user.is_staff
        else:
            return False

