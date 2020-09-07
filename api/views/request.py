from api.models import Request, Project, User, Proposal, Notification
from rest_framework import viewsets, permissions
from api.serializers import RequestSerializer, ProjectSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from json.decoder import JSONDecodeError
import json
from django.http.response import JsonResponse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, action)
from ..authentication import ExpiringTokenAuthentication, IsEmitterOrReadOnly, IsEmitterOrOwnerOfProject
from rest_framework.permissions import IsAuthenticated
from django.core.paginator import Paginator
from ..utils import DEFAULT_IMAGE_URL, send_notification, get_profile_image_id, create_stages, censor_text
from ..tbk_utils import create_payment_order


class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = [IsEmitterOrOwnerOfProject & IsEmitterOrReadOnly & IsAuthenticated]
    total_pages = 0
    out_pag = 1
    http_method_names = ['get', 'patch', 'delete', 'post']

    def list(self, request):
        requests = self.get_queryset()
        pages = Paginator(requests.order_by('created_at').reverse(), 10)
        self.out_pag = 1
        self.total_pages = pages.num_pages
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    self.out_pag = page_asked
        request_list = pages.page(self.out_pag).object_list
        serializer = self.serializer_class(request_list, many=True)
        ResponseData = serializer.data
        
        if 'emitter' in self.request.query_params.keys() or 'project' in self.request.query_params.keys():
            for request in ResponseData:
                if 'emitter' in self.request.query_params.keys():
                    project = Project.objects.get(id = request['project'])
                    user = UserSerializer(User.objects.get(email = project.owner))
                elif 'project' in self.request.query_params.keys():
                    user = UserSerializer(User.objects.get(id = request['emitter']))
                request['user_data'] = user.data
                get_profile_image_id(request['user_data'], request['user_data']['id'])

        headers = self.get_success_headers(serializer.data)
        return Response({'total_pages': self.total_pages, 'actual_page': self.out_pag, 'objects': ResponseData}, status=status.HTTP_200_OK, headers=headers)

    def get_queryset(self):
        self.queryset = Request.objects.all()
        requests = self.queryset
        if 'emitter' in self.request.query_params.keys():
            emitter = self.request.query_params['emitter']
            requests = Request.objects.filter(emitter=emitter)
        if 'project' in self.request.query_params.keys():
            project = self.request.query_params['project']
            requests = Request.objects.filter(project=project)
        if 'reciever' in self.request.query_params.keys():
            projects = Project.objects.filter(owner=self.request.query_params['reciever']).values('id')
            requests = Request.objects.none()
            for id in projects:
                requests_unfiltered = Request.objects.filter(project=id['id'])
                requests |= requests_unfiltered
        return requests

        
    def create(self, request):
        try:
            data = json.loads(request.body)
        except JSONDecodeError as error:
            return JsonResponse({'Request error': str(error)},
                                status=400)
        project = Project.objects.get(id = data['project'])
        if project:
            if project.status == 'published':
                if project.owner.id != data['emitter']:
                    if User.objects.get(id=data['emitter']).is_identity_verified:
                        notifications = Notification.objects.filter(owner=data['emitter'], text_type='service', text_number=1, class_id=data['project'])
                        if len(notifications) > 0:
                            data['invited'] = True
                        data['why_you'] = censor_text(data['why_you'])
                        data['requirements'] = censor_text(data['requirements'])
                        serializer = RequestSerializer(data = data)
                        if serializer.is_valid():
                            instance = serializer.save()
                            requestData = serializer.data
                            send_notification('project', 1, 'project', project.id , project.owner.id)
                            response = {'status_code': 201, 'request': requestData}
                            return JsonResponse(response, status=201)
                        return JsonResponse({'status_text': str(serializer.errors)}, status=400)
                    return JsonResponse({'status_text': "No puedes postular a un proyecto si no haz verificado tu identidad"},
                            status=400)
                return JsonResponse({'status_text': "No puedes postular a tu propio proyecto"},
                            status=400)
            return JsonResponse({'status_text': "Este proyecto ya no acepta postulaciones"},
                            status=400)
        else:
            return JsonResponse({'status_text': "El proyecto no existe!"},
                            status=400)

    def partial_update(self, request, *args, **kwargs):
            self.queryset = Request.objects.all()
            req = self.get_object()
            if 'status' in request.data.keys() and request.data['status'] in ['created', 'accepted', 'rejected']:
                if req.status == 'created':
                    if request.data['status'] == 'accepted':
                        proposals = Proposal.objects.filter(request=req.id, accepted=True)
                        if len(proposals) > 0:
                            project_req = Request.objects.all().filter(project=req.project).exclude(id=req.id)
                            for r in project_req:
                                serializer = self.serializer_class(r, data={"status": 'rejected'}, partial = True)
                                if serializer.is_valid():
                                    serializer.save()
                                else:
                                    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                                send_notification('request-collaborator', 1, 'none', 0 , r.emitter.id)
                            send_notification('request-collaborator', 6, 'project', req.project.id , req.emitter.id)
                            create_stages(proposals[0], req.project.id)
                            create_payment_order(proposals[0], req.project.id)
                        else:
                            return JsonResponse({'status_text': "Todavía no se llega a un acuerdo de negociación."}, status.HTTP_400_BAD_REQUEST)
                    serializer = self.serializer_class(req, data=request.data, partial = True)
                    if serializer.is_valid():
                        serializer.save()
                        project = Project.objects.get(id=req.project.id)
                        p_serializer = ProjectSerializer(project, data={"collaborator_id": req.emitter.id, 'status': 'payment'}, partial = True)
                        if p_serializer.is_valid():
                            p_serializer.save()
                        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                    
                    else:
                        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                elif req.status == 'accepted' and request.data['status'] == 'created':
                    project_req = Request.objects.filter(project=req.project)
                    for r in project_req:
                        serializer = self.serializer_class(r, data={"status": 'created'}, partial = True)
                        if serializer.is_valid():
                            serializer.save()
                        else:
                            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                serializer = self.serializer_class(req, data=request.data, partial = True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                serializer = self.serializer_class(req, data=request.data, partial = True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

