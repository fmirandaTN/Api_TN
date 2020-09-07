from datetime import datetime, date, timedelta
from django.db import models

class ProjectStage(models.Model):
    project = models.ForeignKey(
        'api.Project', related_name="stage", on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    price = models.IntegerField()
    completed = models.BooleanField(default=False)
    aproved = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
