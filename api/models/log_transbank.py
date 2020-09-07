from django.db import models

class LogTransbank(models.Model):
    order = models.ForeignKey(
        'api.Order', on_delete=models.CASCADE, related_name='order', null=True)
    token = models.CharField(max_length=500)
    authorization_code = models.CharField(max_length=500)
    card_number = models.CharField(max_length=500)
    gross_payment = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True) 
    