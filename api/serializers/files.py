from rest_framework import serializers
from api.models import ProjectFile


class ProjectFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectFile
        fields = '__all__'