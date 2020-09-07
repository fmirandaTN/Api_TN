from datetime import datetime
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator


class Request(models.Model):
    status_choices = [
        ('created', 'created'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected')]
    project = models.ForeignKey(
        'api.Project', on_delete=models.CASCADE, related_name='requests', null=True)
    emitter = models.ForeignKey(
        'api.User', on_delete=models.CASCADE, related_name='emitter', null=True)
    
    why_you = models.CharField(max_length=1500)
    requirements = models.CharField(max_length=1500)
    price = models.IntegerField(default=0)
    action_type = models.CharField(max_length=20, default="")
    status = models.CharField(max_length=20, default="created", choices=status_choices)
    invited = models.BooleanField(default=False)
    modified_project = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def project_name(self):
        return self.project.title

    def __str__(self):
        return 'Request de {} en {}'.format(self.emitter, self.project)

    class Meta:
        unique_together = (("emitter", "project"),)
