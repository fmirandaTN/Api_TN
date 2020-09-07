from rest_framework import serializers
from api.models import Project, User, Request


class RequestSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all())
    emitter = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all())
    project_name = serializers.CharField(required=False)

    class Meta:
        model = Request
        fields = ('id', 'project', 'emitter', 'action_type','invited',
                   'status', 'why_you', 'requirements', 'price', 'project_name')
        read_only_fields = ('created_at', 'updated_at')

    