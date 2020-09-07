from rest_framework import serializers
from api.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    text_template = serializers.CharField(required=False)

    class Meta:
        model = Notification
        fields = ('id', 'text_type', 'text_number', 'class_type',
                  'class_id', 'owner', 'text_template', 'viewed')
        read_only_fields = ('created_at',)
