from api.models import ProjectStage
from api.serializers import ProjectStageSerializer, ProjectSerializer
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
from ..utils import get_profile_image_notification, create_journal_entry

def check_project_finish(project_id):
    stages = ProjectStage.objects.filter(project=project_id)
    all_completed = True
    for stage in stages:
        if not stage.completed and not stage.paid:
            all_completed = False
    if all_completed:
        project = ProjectSerializer(stage.project, data={'status':'completed'}, partial=True) 
        if project.is_valid():
            project.save()
            return True
    return False

class ProjectStageViewSet(viewsets.ModelViewSet):
    queryset = ProjectStage.objects.all()
    serializer_class = ProjectStageSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete']

    # def list(self, request):
    #     notifications = self.get_queryset()
    #     pages = Paginator(notifications.order_by('created_at').reverse(), 10)
    #     self.out_pag = 1
    #     self.total_pages = pages.num_pages
    #     self.count_objects = pages.count
    #     if self.request.query_params.keys():
    #         if 'page' in self.request.query_params.keys():
    #             page_asked = int(self.request.query_params['page'])
    #             if page_asked in pages.page_range:
    #                 self.out_pag = page_asked
    #     negotiation_list = pages.page(self.out_pag).object_list
    #     serializer = self.serializer_class(negotiation_list, many=True)
    #     ResponseData = serializer.data
    #     # get_profile_image_notification(ResponseData, 0)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response({'total_pages': self.total_pages,'total_objects':self.count_objects,'actual_page': self.out_pag, 'objects': serializer.data}, status=status.HTTP_200_OK, headers=headers)

    def get_queryset(self):
        self.queryset = ProjectStage.objects.all()
        stages = self.queryset
        if 'project' in self.request.query_params.keys():
            project = self.request.query_params['owner']
            stages = project.filter(project=project)
        return stages

    
    def partial_update(self, request, *args, **kwargs):
        self.queryset = ProjectStage.objects.all()
        stage = self.get_object()
        print(request.data)
        if 'completed' in request.data.keys():
            print(request.data)
            if request.data['completed'] == True:
                serializer = self.serializer_class(stage, data={"completed": True}, partial = True)
                if serializer.is_valid():
                    serializer.save()
                    create_journal_entry(1, serializer.data['project'])
                    data = serializer.data
                    data["project_completed"] = check_project_finish(stage.project.id)
                    return Response(data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
        if 'paid' in request.data.keys():
            if request.data['paid'] == True:
                serializer = self.serializer_class(stage, data={"paid": True}, partial = True)
                if serializer.is_valid():
                    serializer.save()
                    create_journal_entry(2, serializer.data['project'])
                    data = serializer.data
                    data["project_completed"] = check_project_finish(stage.project.id)
                    return Response(data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                
        return JsonResponse({'status_test': "No se puede editar los otros campos de la negociación."},
                    status=400)