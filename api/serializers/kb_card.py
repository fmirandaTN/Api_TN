from rest_framework import serializers
from api.models import KbCard


class KbCardSerializer(serializers.ModelSerializer):

    class Meta:
        model = KbCard
        fields = ('id', 'project', 'status', 'title', 'content', 'issueType',
                'priority', 'estimate', 'position')
