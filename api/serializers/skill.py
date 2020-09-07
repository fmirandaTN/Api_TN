from rest_framework import serializers
from api.models import Skill, Category


class SkillSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(required=False)

    class Meta:
        model = Skill
        fields = ('id', 'name', 'category', 'category_name')
