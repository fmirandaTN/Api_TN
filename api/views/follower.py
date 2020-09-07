from rest_framework import viewsets, permissions
from api.models import Follower, User
from api.serializers import FollowerSerializer, UserSerializer
from django.http.response import JsonResponse
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, action)
from ..authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ebdjango.storage_backends import ProjectFileStorage
import os


class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'delete', 'post']

    

