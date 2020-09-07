from api.models import ProjectJournal
from api.serializers import ProjectJournalSerializer
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from json.decoder import JSONDecodeError
import json
from django.http.response import JsonResponse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, action)
from ..authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from ..utils import get_profile_image_notification

class ProjectJournalViewSet(viewsets.ModelViewSet):
    queryset = ProjectJournal.objects.all()
    serializer_class = ProjectJournalSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        self.queryset = ProjectJournal.objects.all()
        journals = self.queryset
        if 'project' in self.request.query_params.keys():
            project = self.request.query_params['project']
            journals = journals.filter(project=project)
        return journals