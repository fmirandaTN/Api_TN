from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db.models.signals import post_save
from django.db import models
from django.utils import timezone
import datetime
from api.models import Project
from api.models.rating import Rating



class User(AbstractUser):
    ## Register need
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    ## Information to complete
    skills = ArrayField(
        models.CharField(max_length=30), default=list)
    profession = models.CharField(max_length=500, default='')
    about_me = models.CharField(max_length=1500, default="")
    experience = models.CharField(max_length=1500, default="")
    may_interested = models.CharField(max_length=1500, default="")
    phone_number = models.CharField(max_length=15, default= "")

    ## Confirmation
    # is_email_verified = models.BooleanField(default=False)
    is_identity_verified = models.BooleanField(default=False)
    is_account_verified = models.BooleanField(default=False)


    ## Data
    register_status = models.IntegerField(default=0)
    is_admin = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    ## Stats
    recomended = models.IntegerField(default=0)
    completed_works = models.IntegerField(default=0)

    ##Images
    profile_image = models.CharField(max_length=100, default='')
    default_image = models.IntegerField(default=1)
    # USERNAME_FIELD = 'id'

    def client_rating(self):
        projects = Project.objects.filter(owner=self.id).values('id')
        if len(projects) == 0:
            return 0
        sum = 0
        num_ratings = 0
        for id in projects:
            ratings_unfiltered = Rating.objects.filter(rating_type='client', project_id=id['id']).values('rating_average')
            if len(ratings_unfiltered) > 0:
                sum += ratings_unfiltered[0]['rating_average']
                num_ratings += 1
        if num_ratings > 0:
            return sum/num_ratings
        else:
            return 0

    def collaborator_rating(self):
        projects = Project.objects.filter(owner=self.id).values('id')
        if len(projects) == 0:
            return 0
        sum = 0
        num_ratings = 0
        for id in projects:
            ratings_unfiltered = Rating.objects.filter(rating_type='collaborator', project_id=id['id']).values('rating_average')
            if len(ratings_unfiltered) > 0:
                sum += ratings_unfiltered[0]['rating_average']
                num_ratings += 1
        if num_ratings > 0:
            return sum/num_ratings
        else:
            return 0

    def overall_rating(self):
        return (self.client_rating() + self.collaborator_rating()) / 2


    def completed_works(self):
        return len(Project.objects.filter(owner=self.id, status='completed'))

    def outstanding_user(self):
        result = self.completed_works() > 10
        if isinstance(result, bool):
            return result
        else:
            return False

    def publish(self):
        self.save()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        return super(User, self).save(*args, **kwargs)

