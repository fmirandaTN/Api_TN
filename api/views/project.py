from api.models import Project, User, Request, Question, Rating, ProjectJournal, Order, ProjectFile
from rest_framework import viewsets
from api.serializers import ProjectSerializer, QuestionSerializer, RatingSerializer, ProjectJournalSerializer, OrderSerializer, ProjectFileSerializer
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
from django.core.paginator import Paginator
from ..utils import DEFAULT_IMAGE_URL, send_notification, get_profile_image_id, add_user_data, add_progress_data, censor_text, add_stages_data
from django.db.models import Q


def add_project_info(project, owner, request):
    ## Adding questions
    if project['status'] == 'published' or project['status'] == 'selection':
        if owner:
            questions = QuestionSerializer(Question.objects.filter(project=project['id']), many=True).data
        else:
            if request.user:
                owner_query =  Q(project=project['id'],emitter= request.user.id, visible = False)
                visible_query = Q(project=project['id'], visible=True)
                questions = QuestionSerializer(Question.objects.filter(owner_query | visible_query), many=True).data
            else:
                questions = QuestionSerializer(Question.objects.filter(project=project['id'], visible=True), many=True).data
        project['questions']= questions

    ## Adding order for payment
    if project['status'] == 'payment':
        project['order'] = OrderSerializer(Order.objects.filter(project=project['id']), many=True).data

    ## Adding user and progress ddata
    if project['status'] == 'in_progress' or project['status'] == 'payment' or project['status'] == 'completed':
        add_user_data(project, project['collaborator_id'])
        get_profile_image_id(project['user_data'], project['collaborator_id'])
        add_progress_data(project)

    ## Adding files
    if project['status'] == 'in_progress' or project['status'] == 'completed':
        project['files'] = ProjectFileSerializer(ProjectFile.objects.filter(project=project['id']), many=True).data

    ## Adding ratings
    if project['status'] == 'completed':
        ratings = RatingSerializer(Rating.objects.filter(project=project['id']), many=True).data
        client_rating = False
        collaborator_rating = False
        for rate in ratings:
            if rate['rating_type'] == 'client':
                client_rating = True
            if rate['rating_type'] == 'collaborator':
                collaborator_rating = True
        project['ratings'] = ratings
        project['cient_rating'] = client_rating
        project['collaborator_rating'] = collaborator_rating

def add_rating_data(project):	
    ratings = RatingSerializer(Rating.objects.filter(project=project['id']), many=True).data
    client_rating = False
    collaborator_rating = False
    for rate in ratings:
        if rate['rating_type'] == 'client':
            client_rating = True
        if rate['rating_type'] == 'collaborator':
            collaborator_rating = True
    project['ratings'] = ratings
    project['cient_rating'] = client_rating
    project['collaborator_rating'] = collaborator_rating


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = [IsOwnerOrReadOnly, ProjectStatus, IsAuthenticatedOrReadOnly]
    out_pag = 1
    total_pages = 0
    count_objects = 0
    http_method_names = ['get', 'patch', 'delete']

    def retrieve(self, request, pk):
        self.queryset = Project.objects.all()
        project = self.get_object()
        if request.user != project.owner:
            views = project.visits + 1
            serializer = ProjectSerializer(project, data={'visits': views}, partial = True)
            if serializer.is_valid():
                serializer.save()
            owner = False
        else:
            serializer = ProjectSerializer(project)
            owner = True
        project = serializer.data
        add_project_info(project, owner, request)
        return Response(project)

    def list(self, request):
        projects = self.get_queryset()
        pages = Paginator(projects.order_by('created_at').reverse(), 10)
        self.out_pag = 1
        self.total_pages = pages.num_pages
        self.count_objects = pages.count
        if self.request.query_params.keys():
            if 'page' in self.request.query_params.keys():
                page_asked = int(self.request.query_params['page'])
                if page_asked in pages.page_range:
                    self.out_pag = page_asked
        project_list = pages.page(self.out_pag).object_list
        serializer = self.serializer_class(project_list, many=True)
        ResponseData = serializer.data
        for project in ResponseData:
            get_profile_image_id(project, project['owner'])
            if self.request.query_params.keys():	
                if 'user_completed' in self.request.query_params.keys():	
                    add_rating_data(project)
                if 'my_projects' in self.request.query_params.keys():
                    add_stages_data(project)
        headers = self.get_success_headers(serializer.data)
        return Response({'total_pages': self.total_pages,'total_objects':self.count_objects,'actual_page': self.out_pag, 'objects': serializer.data}, status=status.HTTP_200_OK, headers=headers)


    def get_queryset(self):
        self.queryset = Project.objects.all()
        projects = self.queryset
        if self.request.query_params.keys():
            if 'category' in self.request.query_params.keys():
                categories = self.request.query_params.getlist(key='category')
                projects_none = Project.objects.none()
                for project in projects:
                    for i in categories:
                        if int(i) in project.categories:
                            projects_none |= Project.objects.filter(id=project.id)
                            break
                projects = projects_none
                
            if 'sub-category' in self.request.query_params.keys():
                subcategories = self.request.query_params.getlist(key='sub-category')
                projects_none = Project.objects.none()
                for project in projects:
                    for i in subcategories:
                        if int(i) in project.categories:
                            projects_none |= Project.objects.filter(id=project.id)
                            break
                projects = projects_none                

            if 'min_price' in self.request.query_params.keys():
                min_price = int(self.request.query_params['min_price'])
                projects = projects.filter(
                    min_price_range__gte=min_price)

            if 'max_price' in self.request.query_params.keys():
                max_price = int(self.request.query_params['max_price'])
                projects = projects.filter(
                    max_price_range__lte=max_price)

            if 'modality' in self.request.query_params.keys():
                options = ['fulltime', 'parttime', 'mixed', 'homeoffice']
                project_modality = self.request.query_params.getlist(key='modality')
                for modality in options:
                    if modality not in project_modality:
                        projects = projects.exclude(work_modality=modality)

            if 'owner' in self.request.query_params.keys():
                owner = self.request.query_params['owner']
                projects = projects.filter(owner=owner)

            if 'collaborator' in self.request.query_params.keys():
                collaborator = self.request.query_params['collaborator']
                projects = projects.exclude(status='published').filter(collaborator_id=collaborator)
                
            if 'status' in self.request.query_params.keys():
                options = ['completed', 'published', 'in_progress', 'selection', 'payment']
                project_status = self.request.query_params.getlist(key='status')
                for status in options:
                    if status not in project_status:
                        projects = projects.exclude(status=status)

            if 'skill' in self.request.query_params.keys():
                skills = self.request.query_params.getlist(key='skill')

                projects_none = Project.objects.none()
                for project in projects:
                    for skill in skills:
                        if int(skill) in project.skills_required:
                            projects_none |= Project.objects.filter(id=project.id)
                            break
                projects = projects_none

            if 'search' in self.request.query_params.keys():
                name_query = Q(title__iregex=r"(^|\s)%s" % self.request.query_params['search'])
                text_query = Q(description__contains=self.request.query_params['search'])
                projects = projects.filter(name_query | text_query)
        
            if 'user_completed' in self.request.query_params.keys():	
                client_query = Q(owner = self.request.query_params['user_completed'])	
                collaborator_query =  Q(collaborator_id = self.request.query_params['user_completed'])	
                projects = projects.filter(status='completed').filter(client_query | collaborator_query)

            if 'my_projects' in self.request.query_params.keys():
                client_query = Q(owner = self.request.query_params['my_projects'])	
                collaborator_query =  Q(collaborator_id = self.request.query_params['my_projects'])
                projects = projects.filter(client_query | collaborator_query).exclude(status='selection').exclude(status='published')

            
        return projects

    def partial_update(self, request, *args, **kwargs):
        self.queryset = Project.objects.all()
        project = self.get_object()
        modify_status = False
        if 'status' in request.data.keys():
            modify_status = True
        serializer = ProjectSerializer(project, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            if serializer.data['status'] == 'published' and not modify_status:
                requests = Request.objects.filter(project=serializer.data['id'])
                for req in requests:
                    send_notification('request-collaborator', 5, 'project', serializer.data['id'], req.emitter.id)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def registerProject(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError as error:
        return JsonResponse({'status_text': "Error en el body del request", 'error': str(error)},
                            status=400)
    owner = User.objects.get(id=data['owner'])
    if owner:
        if owner.is_account_verified:
            data['description'] = censor_text(data['description'])
            serializer = ProjectSerializer(data=data)
            if serializer.is_valid():
                instance = serializer.save()
                projectData = serializer.data
                response = {'status_code': 201, 'project': projectData}
                return JsonResponse(response, status=201)
            return JsonResponse({'status_text': str(serializer.errors)}, status=400)
        return JsonResponse({'status_text': "Se necesita verificar la cuenta identidad para poder publicar"},
                        status=400)
    return JsonResponse({'status_text': "Este cliente no existe!"},
                        status=400)

