from rest_framework import permissions

class UserViewSetPermission(permissions.BasePermission):
    """
        every authenticate user can : get 
        only admin can destory, create,
    """ 
    def has_permission(self, request, view):
        print('vie2w', view.action, request.user)
        if not request.user.is_authenticated or view.action == 'create' :
            return False
        if view.action in ['blockuser', 'unblockuser', 'list', 'mine', 'admin_accept']:
            return True
        elif view.action in [ 'retrieve', 'update', 'partial_update', 'destroy']:
            return True
        elif view.action in ['user_profile_pic', 'user_profile_bio', 'accept_profile_pic']:
            return request.user.is_admin or request.user.is_staff
        else:
            return False
                                                                                                
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated or view.action == 'create':
            return False
        if view.action in ['unblockuser', 'blockuser', 'retrieve']:
            return True
        elif view.action in [ 'update', 'partial_update']:
            return obj == request.user or request.user.is_admin or request.user.is_staff
        elif view.action in ['destroy', 'change_status', 'accept_profile_pic', 'user_profile_pic', 'user_profile_bio']:
            return request.user.is_admin or request.user.is_staff
        else:
            return False






