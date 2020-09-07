from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from api.models import Project


class Question(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    emitter =  models.ForeignKey(
        'api.User', related_name="emitter_question", on_delete=models.CASCADE)
    question_text = models.CharField(max_length=1000)
    answer_text =  models.CharField(max_length=1000, null=True)
    visible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)