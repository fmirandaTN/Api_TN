from rest_framework import serializers
from api.models import Question

class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = ('id', 'project', 'emitter', 'question_text', 'answer_text', 'visible')
        read_only_fields = ('created_at', 'updated_at')
