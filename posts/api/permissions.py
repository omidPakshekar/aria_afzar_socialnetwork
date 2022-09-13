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
        if view.action in ['get_comment', 'add_like', 'add_user_saved', 'admin_accept' ,'add_comment', 'mine', 'add_listen']:
            return True
        elif view.action in ['mine_count', 'history', 'create', 'retrieve', 'partial_update', 'destroy', 'update', 'get_count','add_project']:
            return True
        elif view.action in ['admin_check', 'change_money_unit', 'show_money_unit']:
            return request.user.is_admin or request.user.is_staff
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        if view.action in ['retrieve']:
            return True
        if not request.user.is_authenticated:
            return False
        if view.action in ['get_comment', 'add_project', 'add_like', 'add_user_saved' ,'add_comment', 'add_listen']:
            return True
        elif view.action in [ 'update', 'partial_update', 'destroy']:
            return obj.owner == request.user or request.user.is_admin or request.user.is_staff
        elif view.action in [ 'change_status', 'admin_accept', 'get_count', 'admin_check']:
            return request.user.is_admin or request.user.is_staff
        else:
            return False


class ProjectPermission(permissions.BasePermission):
    """
        every authenticate user can :create, 
        only admin can destory
        retreive, update : if you are admin or owner
        
    """ 
    
    def has_permission(self, request, view):
        if  request.user.is_anonymous:
            return False
        if view.action in ['list', 'retrieve', 'show_requests', 'add_request', 'accept_user', 'mine']:
            return True
        elif view.action =='admin_check':
            return request.user.is_admin or request.user.is_staff
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        if request.user.is_anonymous:
            return False
        elif view.action in [ 'update', 'partial_update', 'accept_user']:
            return obj.owner == request.user or request.user.is_admin or request.user.is_staff
        elif view.action in ['destroy', 'admin_accept']:
            return request.user.is_admin or request.user.is_staff
        elif view.action in ['show_requests', 'add_request', 'retrieve']:
            return True
        else:
            return False

