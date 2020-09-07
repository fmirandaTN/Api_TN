from rest_framework import serializers
from api.models import ProjectJournal


class ProjectJournalSerializer(serializers.ModelSerializer):
    text_template = serializers.CharField(required=False)

    class Meta:
        model = ProjectJournal
        fields = ('project', 'entry', 'text_template', 'created_at')
        read_only_fields = ('created_at',)