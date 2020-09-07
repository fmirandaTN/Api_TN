from api.models import Notification
from rest_framework import viewsets, permissions
from api.serializers import NotificationSerializer
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

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    out_pag = 1
    total_pages = 0
    count_objects = 0

    def list(self, request):
        notifications = self.get_queryset()
        pages = Paginator(notifications.order_by('created_at').reverse(), 10)
        self.out_pag = 1
        self.total_pages = pages.num_pages
        self.count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    self.out_pag = page_asked
        negotiation_list = pages.page(self.out_pag).object_list
        serializer = self.serializer_class(negotiation_list, many=True)
        ResponseData = serializer.data
        get_profile_image_notification(ResponseData)
        headers = self.get_success_headers(serializer.data)
        Notification.objects.filter(owner=self.request.query_params['owner']).filter(viewed=False).update(viewed=True)
        return Response({'total_pages': self.total_pages,'total_objects':self.count_objects,'actual_page': self.out_pag, 'objects': serializer.data}, status=status.HTTP_200_OK, headers=headers)


    def get_queryset(self):
        self.queryset = Notification.objects.all()
        notifications = self.queryset
        if 'owner' in self.request.query_params.keys():
            owner = self.request.query_params['owner']
            notifications = notifications.filter(owner=owner)
        return notifications