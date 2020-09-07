from api.models import Question, Project
from rest_framework import viewsets
from api.serializers import QuestionSerializer
from django.http.response import JsonResponse
from json.decoder import JSONDecodeError
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, action)
from ..authentication import ExpiringTokenAuthentication, IsOwnerOrReadOnly, ProjectStatus
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
# from django.core.paginator import Paginator
from ..utils import send_notification, censor_text
# from django.db.models import Q

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    # permission_classes = [IsOwnerOrReadOnly, ProjectStatus, IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        self.get_queryset = Question.objects.all()
        questions = self.queryset
        if 'project' in self.request.query_params.keys():
            project = self.request.query_params['project']
            questions = questions.filter(project = project)
        if 'visible' in self.request.query_params.keys():
            visible = self.request.query_params['project']
            questions = questions.filter(visible=visible)
        return questions

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
                    serializer = self.serializer_class(data=data)
                    if serializer.is_valid():
                        instance = serializer.save()
                        questionData = serializer.data
                        send_notification('project', 3, 'project', project.id , project.owner.id)
                        response = {'status_code': 201, 'request': questionData}
                        return JsonResponse(response, status=201)
                    return JsonResponse({'status_text': str(serializer.errors)}, status=400)
            return JsonResponse({'status_text': "Este proyecto ya no acepta preguntas"},
                            status=400)
        else:
            return JsonResponse({'status_text': "El proyecto no existe!"},
                            status=400)


    def partial_update(self, request, *args, **kwargs):
        self.queryset = Question.objects.all()
        question = self.get_object()
        if 'answer_text' in request.data.keys():
            serializer = self.serializer_class(question, data={"answer_text":request.data['answer_text'],"visible": True}, partial = True)
            if serializer.is_valid():
                instance = serializer.save()
                questionData = serializer.data 
                send_notification('request-collaborator', 7, 'project', question.project.id , questionData['emitter'])
                response = {'status_code': 201, 'request': questionData}
                return JsonResponse(response, status=201)
            return JsonResponse({'status_text': str(serializer.errors)}, status=400)
        return JsonResponse({'status_text': "No se pueden editar estos campos de la pregunta"},
                        status=400)