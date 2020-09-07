from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied
from rest_framework import permissions
from django.utils import timezone
from django.conf import settings
from api.models.user import User


class ExpiringTokenAuthentication(TokenAuthentication):
    """
    If token is expired then it will be removed
    and new one with different key will be created
    """

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid Token")

        if not token.user.is_active:
            raise AuthenticationFailed("User is not active")

        time_elapsed = timezone.now() - token.created

        if settings.TOKEN_EXPIRE_TIME < time_elapsed:
            raise AuthenticationFailed('Token has expired')
        
        return (token.user, token)

class IsOwnerOrReadOnly(permissions.BasePermission):
    

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user

class IsUserOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True
        # print(obj, request.user)
        # Write permissions are only allowed to the owner of the snippet.
        return obj == request.user

class IsEmitterOrReadOnly(permissions.BasePermission):
    

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        if obj.emitter == request.user:
            return True
        elif obj.project.owner == request.user:
            return True
        else:
            return False


class IsRatingEmitter(permissions.BasePermission):
    

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        if obj.project.rating_type == 'collaborator':
            print(obj.project.owner, request.user)
            return obj.project.owner == request.user
        elif obj.project.rating_type == 'client':
            print(obj.project.collaborator, request.user.id)
            return obj.project.collaborator == request.user.id
        return False

class IsEmitterOrOwnerOfProject(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if obj.emitter == request.user:
                return True
            elif obj.project.owner == request.user:
                return True
            return False
        else:
            return True

class ProjectStatus(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if obj.status == 'published' or obj.status == 'selection':
            return True
        elif obj.status == 'in_progress' or obj.status == 'completed':
            if obj.collaborator_id:
                collaborator = User.objects.get(id=obj.collaborator_id)
            else:
                collaborator = 'NULL'
            print('{}={} or {}={}'.format(request.user, obj.owner, request.user, collaborator))
            if request.user == obj.owner or request.user == collaborator:
                return True
            else:
                raise PermissionDenied()
        elif obj.status == 'payment':
            return request.user == obj.owner


class IsEmitterOrReadOnlyProposal(permissions.BasePermission):
    

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        elif request.method == 'PATCH':
            # print((obj.emitter != request.user and obj.request.emitter == request.user), (obj.emitter != request.user and obj.request.project.owner  == request.user))
            # print(obj.emitter, request.user, obj.request.emitter, request.user, obj.request.project.owner, request.user)
            if (obj.emitter != request.user and obj.request.emitter == request.user) or (obj.emitter != request.user and obj.request.project.owner  == request.user):
                return True
        else:
            return obj.emitter == request.user
            
        return False