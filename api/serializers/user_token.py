from rest_framework import serializers
from api.models import UserToken

class UserTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserToken
        fields = ('owner', 'token', 'validation', 'recovery')