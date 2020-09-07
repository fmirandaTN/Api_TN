from rest_framework import serializers
from api.models import User
from rest_framework.authtoken.models import Token
from .FlexFieldsModelSerializer import FlexFieldsModelSerializer
from django.core.exceptions import ObjectDoesNotExist


class UserSerializer(FlexFieldsModelSerializer):
    password = serializers.CharField(write_only=True)
    client_rating = serializers.FloatField(required=False)
    collaborator_rating = serializers.FloatField(required=False)
    overall_rating = serializers.FloatField(required=False)
    outstanding_user = serializers.BooleanField(required=False)
    completed_works = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'is_superuser',
                  'first_name', 'last_name', 'is_active',
                  'password', 'created_at', 'updated_at',
                  'deleted', 'last_login', 'register_status',
                  'skills', 'about_me', 'experience', 'may_interested',
                  'client_rating', 'profile_image',  'outstanding_user',
                  'recomended' , 'completed_works', 'collaborator_rating',
                   'overall_rating', 'default_image', 'profession')
        read_only_fields = ('deleted', 'created_at', 'updated_at',  'outstanding_user')

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


    def save(self, *args, **kwargs):
        instance = super(UserSerializer, self).save(*args, **kwargs)
        token = Token.objects.get_or_create(user=instance)
        if instance.deleted:
            token.delete()
        return instance, token

    def get_token(self):
        try:
            token = Token.objects.get(user=self.instance)
        except ObjectDoesNotExist:
            token = Token.objects.create(user=self.instance)
        return token

    def new_token(self):
        Token.objects.filter(user=self.instance).delete()
