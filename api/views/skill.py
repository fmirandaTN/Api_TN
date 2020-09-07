from api.models import Skill
from rest_framework import viewsets, permissions
from api.serializers import SkillSerializer
from rest_framework.permissions import IsAuthenticated
from ..authentication import ExpiringTokenAuthentication


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    http_method_names = ['get']
    
    def get_queryset(self):
        self.queryset = Skill.objects.all()
        skills = self.queryset
        if self.request.query_params.keys():
                if 'category' in self.request.query_params.keys():
                    skills = Skill.objects.filter(category=self.request.query_params['category'])

                if 'search' in self.request.query_params.keys():
                    skills = Skill.objects.filter(name__iregex=r"(^|\s)%s" % self.request.query_params['search'])
        return skills

