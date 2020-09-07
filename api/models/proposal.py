from django.db import models
from django.contrib.postgres.fields import ArrayField

class Proposal(models.Model):

    emitter = models.ForeignKey(
        'api.User', on_delete=models.CASCADE, related_name='proposal_emitter')
    request = models.ForeignKey(
        'api.Request', on_delete=models.CASCADE, related_name='proposal_request')
    accepted = models.BooleanField(default=False)
    stages = ArrayField(
        models.CharField(max_length=30), default=list, null=True)
    prices =  ArrayField(
        models.IntegerField(), default=list, null=True)
    text = models.CharField(max_length=1000)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def total_price(self):
        total = 0
        for p in self.prices:
            total += p
        return total