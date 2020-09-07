from rest_framework import serializers
from api.models import Service, User


class ServiceSerializer(serializers.ModelSerializer):
    categories_names = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
    skills_names = serializers.ListField(child=serializers.CharField(max_length=50), required=False)
    owner_username = serializers.CharField(required=False)

    class Meta:
        model = Service
        fields = ('id', 'title', 'description', 'skills_required',
                  'experience', 'availability', 'work_modality',
                  'owner', 'owner_username', 'min_price_range', 
                  'max_price_range', 'status', "categories", 'visits',
                  'categories_names','skills_names')

        read_only_fields = ('created_at', 'updated_at')
