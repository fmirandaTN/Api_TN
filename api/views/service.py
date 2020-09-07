from api.models import Service, User, Picture, Project
from rest_framework import viewsets, permissions
from api.serializers import ServiceSerializer, PictureSerializer
from django.http.response import JsonResponse
from json.decoder import JSONDecodeError
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from ..authentication import ExpiringTokenAuthentication
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, action)
from ..authentication import ExpiringTokenAuthentication, IsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from ..utils import DEFAULT_IMAGE_URL, send_notification, censor_text
from django.db.models import Q


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
    out_pag = 1
    total_pages = 0
    count_objects = 0
    http_method_names = ['get', 'patch', 'delete']

    def retrieve(self, request, pk):
        queryset = Service.objects.all()
        service = self.get_object()
        if request.user != service.owner:
            views = service.visits + 1
            serializer = self.serializer_class(service, data={'visits': views}, partial = True)
            if serializer.is_valid():
                serializer.save()
        else:
            serializer = self.serializer_class(service)
        service = serializer.data
        return Response(service)

    def list(self, request):
        services = self.get_queryset()
        pages = Paginator(services.order_by('created_at').reverse(), 10)
        self.out_pag = 1
        self.total_pages = pages.num_pages
        self.count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    self.out_pag = page_asked
        service_all = pages.page(self.out_pag).object_list

        serializer = self.serializer_class(service_all, many=True)
        ResponseData = serializer.data
        for service in ResponseData:
            pic = Picture.objects.filter(owner=service['owner'])
            if len(pic) > 0:
                picture = PictureSerializer(pic[0]).data
                service['profile_image'] = picture['storage_url']
            else:
                service['profile_image'] = DEFAULT_IMAGE_URL.format(User.objects.get(id = service['owner']).default_image)
        
        headers = self.get_success_headers(serializer.data)
        return Response({'total_pages': self.total_pages, 'total_objects':self.count_objects, 'actual_page': self.out_pag, 'objects': serializer.data}, status=status.HTTP_200_OK, headers=headers)


    def get_queryset(self):
        self.queryset = Service.objects.all()
        services = self.queryset
        if self.request.query_params.keys():
            if 'min_price' in self.request.query_params.keys():
                min_price = int(self.request.query_params['min_price'])
                services = Service.objects.filter(
                    min_price_range__gte=min_price)
                    
            if 'max_price' in self.request.query_params.keys():
                max_price = int(self.request.query_params['max_price'])
                services = Service.objects.filter(
                    max_price_range__lte=max_price)


            if 'category' in self.request.query_params.keys():
                categories = self.request.query_params.getlist(key='category')
                service_none = Service.objects.none()
                for service in services:
                    for i in categories:
                        if int(i) in service.categories:
                            service_none |= Service.objects.filter(id=service.id)
                            break
                services = service_none
                
            if 'subcategory' in self.request.query_params.keys():
                subcategories = self.request.query_params.getlist(key='sub-category')
                service_none = Service.objects.none()
                for service in services:
                    for i in subcategories:
                        if int(i) in service.subcategories:
                            service_none |= Service.objects.filter(id=service.id)
                            break
                services = service_none

            if 'modality' in self.request.query_params.keys():
                options = ['fulltime', 'parttime', 'mixed', 'homeoffice']
                service_modality = self.request.query_params.getlist(key='modality')
                for modality in options:
                    if modality not in service_modality:
                        services = services.exclude(work_modality=modality)

            if 'owner' in self.request.query_params.keys():
                owner = self.request.query_params['owner']
                services = services.filter(owner=owner)

            if 'status' in self.request.query_params.keys():
                status = self.request.query_params['status']
                if status in ['active', 'inactive']:
                    services = services.filter(status=status)

            if 'skill' in self.request.query_params.keys():
                skills = self.request.query_params.getlist(key='skill')
                # print(skills)
                # conditions = Q(skills_required__contains = skills[0])
                # for skill in skills[1:]:
                #     conditions |= Q(skills_required__contains = skill)
                # projects  = projects.filter(conditions)

                # projects = projects.filter(skills_required__in = skills)

                service_none = Service.objects.none()
                for service in services:
                    for skill in skills:
                        if int(skill) in service.skills_required:
                            service_none |= Service.objects.filter(id=project.id)
                            break
                services = service_none

            if 'search' in self.request.query_params.keys():
                name_query = Q(title__iregex=r"(^|\s)%s" % self.request.query_params['search'])
                text_query = Q(description__contains=self.request.query_params['search'])
                services = services.filter(name_query | text_query)

        return services

    def partial_update(self, request, *args, **kwargs):
        self.queryset = Service.objects.all()
        service = self.get_object()
        serializer = ServiceSerializer(service, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data=user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   

@csrf_exempt
@api_view(['POST'])
def registerService(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError as error:
        return JsonResponse({'status_text': "Error en el body del request", 'error': str(error)},
                            status=400)
    owner = User.objects.get(id=data['owner'])
    if owner:
        if owner.is_account_verified:
            data['description'] = censor_text(data['description'])
            serializer = ServiceSerializer(data=data)
            if serializer.is_valid():
                instance = serializer.save()
                projectData = serializer.data
                response = {'status_code': 201, 'service': projectData}
                return JsonResponse(response, status=201)
            return JsonResponse({'status_text': str(serializer.errors)}, status=400)
        return JsonResponse({'status_text': "Se necesita verificar la cuenta identidad para poder publicar"},
                        status=400)
    return JsonResponse({'status_text': "Este cliente no existe!"},
                        status=400)

@csrf_exempt
@api_view(['POST'])
def inviteService(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError as error:
        return JsonResponse({'status_text': "Error en el cuerpo del request", 'error': str(error)},
                            status=400)
    owner = User.objects.get(id = data['owner'])
    project = Project.objects.get(id = data['project'])
    if owner and project:
        send_notification('service', 1, 'project', project.id, owner.id)
        response = {'status_text':'El usuario fue notificado'}
        return JsonResponse(response, status=201)
    else:
        return JsonResponse({'status_text': "No se pudo encontrar el proyecto o el usuario"},
                        status=400)
        