from datetime import datetime, date, timedelta
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from api.models.request import Request
from api.models.skill import Skill
from api.models.category import Category


class Project(models.Model):
    status_choices = [
        ('published', 'published'),
        ('selection', 'selection'),
        ('in_progress', 'in_progress'),
        ('payment','payment'),
        ('completed', 'completed')]

    modality_choices = [
        ('fulltime','fulltime'),
        ('parttime','parttime'),
        ('mixed','mixed'),
        ('homeoffice','homeoffice')]
        
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1500)
    work_modality = models.CharField(max_length=500, null=True, choices=modality_choices)

    categories = ArrayField(
        models.IntegerField(null=True), default=list)
    skills_required = ArrayField(
        models.IntegerField(null=True), default=list)

    end_postulations = models.DateField(default=(date.today() + timedelta(days=7)))
    owner = models.ForeignKey(
        'api.User', related_name="project", on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price_range = models.IntegerField(default=0)
    max_price_range = models.IntegerField(default=0)
    status = models.CharField(max_length=30, default="published", choices=status_choices)
    collaborator_id = models.IntegerField(null=True)
    experience_required = models.CharField(max_length=100, null=True)
    visits = models.IntegerField(default=0)


    def owner_username(self):
        return self.owner.username

    def n_requests(self):
        return len(Request.objects.filter(project=self.id))

    def categories_names(self):
        names = []
        for category in self.categories:
            names.append(Category.objects.get(id=category).name)
        return names

    def skills_names(self):
        names = []
        for skill in self.skills_required:
            names.append(Skill.objects.get(id=skill).name)
        return names

    def __str__(self):
        return self.title