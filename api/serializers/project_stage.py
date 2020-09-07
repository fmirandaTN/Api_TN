from rest_framework import serializers
from api.models import ProjectStage


class ProjectStageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectStage
        fields = '__all__' 