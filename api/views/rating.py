from api.models import Rating, Project
from rest_framework import viewsets, permissions
import json
from api.serializers import RatingSerializer
from django.http.response import JsonResponse
from django.utils import timezone
from json.decoder import JSONDecodeError
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, action)
from ..authentication import ExpiringTokenAuthentication, IsOwnerOrReadOnly, IsRatingEmitter
from rest_framework.permissions import IsAuthenticated

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = [IsRatingEmitter, IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete', 'post']

    def get_queryset(self):
        self.queryset = Rating.objects.all()
        ratings = self.queryset
        if self.request.query_params.keys():
            if 'rating_type' and 'user_id' in self.request.query_params.keys():
                user_id = self.request.query_params['user_id']
                projects = Project.objects.filter(owner=user_id).values('id')
                ratings = []
                if self.request.query_params['rating_type'] == 'client':
                    for id in projects:
                        ratings_unfiltered = Rating.objects.filter(rating_type='client', project_id=id['id'])
                        ratings += ratings_unfiltered
                elif self.request.query_params['rating_type'] == 'collaborator':
                    for id in projects:
                        ratings_unfiltered = Rating.objects.filter(rating_type='collaborator', project_id=id['id'])
                        ratings += ratings_unfiltered
            
            elif 'project' in self.request.query_params.keys():
                ratings = Rating.objects.filter(project=self.request.query_params['project'])
        return ratings

    def create(self, request):
        try:
            data = json.loads(request.body)
        except JSONDecodeError as error:
            return JsonResponse({'Rating error': str(error)},
                                status=400)
        project = Project.objects.get(id = data['project'])
        if project:
            if project.status == 'completed':
                serializer = RatingSerializer(data = data)
                if serializer.is_valid():
                    instance = serializer.save()
                    ratingData = serializer.data
                    response = {'status_code': 201, 'project': ratingData}
                    return JsonResponse(response, status=201)
                return JsonResponse({'status_text': str(serializer.errors)}, status=400)
                
            return JsonResponse({'status_text': "No se puede evaluar un proyecto que no ha sido completado"},
                            status=400)
        else:
            return JsonResponse({'status_text': "El proyecto no existe!"},
                            status=400)
        







    