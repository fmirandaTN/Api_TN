from datetime import datetime, date, timedelta
from django.db import models

class UserToken (models.Model):
    token = models.CharField(max_length=500)
    owner = models.ForeignKey(
        'api.User', related_name="token_register", on_delete=models.CASCADE, null=True)
    validation = models.BooleanField(default=False)
    recovery = models.BooleanField(default=False)