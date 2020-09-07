from api.models import Picture, User
from rest_framework import viewsets, permissions
import json
from api.serializers import PictureSerializer
from django.http.response import JsonResponse
from django.utils import timezone
from json.decoder import JSONDecodeError
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, action)
from ..authentication import ExpiringTokenAuthentication, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from ebdjango.storage_backends import ProfilePictureStorage, delete_in_folder
import os
import boto3


class PictureViewSet(viewsets.ModelViewSet):
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    http_method_names = ['get', 'post', 'delete']
    
    def create(self, request):
        data = request.data
        user = User.objects.get(id = data['owner'])
        file_obj = data['file']
        file_directory_within_bucket = '{}'.format(user)
        type = file_obj.name.split('.')
        id = 0
        created = Picture.objects.filter(owner = data['owner'])
        if len(created) > 0:
            for pic in created:
                id = pic.id
                pic.delete()
            delete_in_folder(file_directory_within_bucket)

        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            str(user.username) + '_ProfilePicture{}'.format(id) + '.' + type[-1] 
        )
        pps = ProfilePictureStorage()
        pps.save(file_path_within_bucket, file_obj)
        file_url = pps.url(file_path_within_bucket)
       
        picture_data = {'owner': user.id,
                        'path_in_storage': file_path_within_bucket,
                        'storage_url': file_url}
        serializer = self.serializer_class(data = picture_data)
        if serializer.is_valid():
            instance = serializer.save()
            pictureData = serializer.data
            response = {'status_code': 201, 'picture': pictureData}
            return JsonResponse(response, status=201)
        return JsonResponse({'status_text': str(serializer.errors)}, status=400)
