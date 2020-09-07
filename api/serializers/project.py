from rest_framework import serializers
from api.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(required=False)
    n_requests = serializers.IntegerField(required=False)
    categories_names = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
    skills_names = serializers.ListField(child=serializers.CharField(max_length=50), required=False)

    class Meta:
        model = Project
        fields = ('id', 'title', 'description', 'skills_required',
                  'work_modality', 'categories', 'end_postulations',
                  'owner', 'owner_username', 'min_price_range',
                  'max_price_range', 'status', 'experience_required' ,
                  'collaborator_id', 'visits', 'n_requests', 'categories_names',
                  'skills_names')
        read_only_fields = ('created_at', 'updated_at')
