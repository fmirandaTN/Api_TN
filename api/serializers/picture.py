from rest_framework import serializers
from api.models import Picture


class PictureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Picture
        fields = '__all__'