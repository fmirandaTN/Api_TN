from rest_framework import viewsets, permissions
from api.models import ProjectFile, User
from api.serializers import ProjectFileSerializer, UserSerializer
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, action)
from ..authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ebdjango.storage_backends import ProjectFileStorage, delete_file
import os
from ..utils import create_token


class ProjectFileViewSet(viewsets.ModelViewSet):
    queryset = ProjectFile.objects.all()
    serializer_class = ProjectFileSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'delete', 'post']

    def create(self, request):
        data = request.data
        user = User.objects.get(id = data['owner'])
        file_obj = data['file']
        file_type = file_obj.name.split('.')[-1]
        original_name = data['file'].name
        index = 1
        new_name = original_name
        while True:
            if len(ProjectFile.objects.filter(project = data['project'], original_name=new_name)) > 0:
                new_name = original_name
                new_name = '({})'.format(index) + new_name
                index += 1
            else:
                break
        file_directory_within_bucket = 'projectFiles{}'.format(data['project'])
        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            'ProjectFile_' + create_token() + '.' + file_type
        )
        pps = ProjectFileStorage()
        pps.save(file_path_within_bucket, file_obj)
        file_url = pps.url(file_path_within_bucket)
        file_data = {'owner': data['owner'],
                    'upload': file_url,
                    'project': data['project'],
                    'original_name': new_name}

        serializer = self.serializer_class(data = file_data)
        if serializer.is_valid():
            instance = serializer.save()
            fileData = serializer.data
            response = {'status_code': 201, 'data': fileData}
            return JsonResponse(response, status=201)
        return JsonResponse({'status_text': str(serializer.errors)}, status=400)

    def destroy(self, request, *args, **kwargs):
        try:
            file_object = self.get_object()
            file_url = file_object.upload
            delete_file(file_url)
            file_object.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)