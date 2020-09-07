from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator


class KbCard(models.Model):
    project = models.ForeignKey(
        'api.Project', on_delete=models.CASCADE, related_name='project_kanban')
    status = models.CharField(max_length=1000)
    title = models.CharField(max_length=200)
    content = models.CharField(max_length=2000)
    issueType = models.CharField(max_length=200)
    priority = models.CharField(max_length=200)
    estimate = models.CharField(max_length=200)
    position = models.IntegerField()