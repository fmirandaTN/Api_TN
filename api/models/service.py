from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from api.models.skill import Skill
from api.models.category import Category


class Service(models.Model):
    # Activo/inactivo
    status_choices = [
        ('active', 'active'),
        ('inactive', 'inactive')]
        
    modality_choices = [
        ('fulltime','fulltime'),
        ('parttime','parttime'),
        ('mixed','mixed'),
        ('homeoffice','homeoffice')
    ]
    title = models.CharField(max_length=500)
    description = models.CharField(max_length=1500)
    work_modality = models.CharField(max_length=500, choices=modality_choices)
    experience = models.CharField(max_length=1500)
    categories = ArrayField(
        models.IntegerField(null=True), default=list)
    skills_required = ArrayField(
        models.IntegerField(null=True), default=list)
    availability = models.CharField(max_length=1500)

    owner = models.ForeignKey(
        'api.User', related_name="service", on_delete=models.CASCADE, null=True)
    # owner_username = models.CharField(max_length=30, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    min_price_range = models.IntegerField(default=0)
    max_price_range = models.IntegerField(default=0)
    status = models.CharField(max_length=30, default="active", choices=status_choices)
    visits = models.IntegerField(default=0)

    def owner_username(self):
        return self.owner.username

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