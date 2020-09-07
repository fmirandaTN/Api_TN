from django.db import models

class Order(models.Model):
    project = models.ForeignKey(
        'api.Project', on_delete=models.CASCADE, related_name='order', null=True)
    gross_payment = models.IntegerField()
    order_number =  models.IntegerField(unique=True)
    payment_type = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True) 
    paid = models.BooleanField(default=False)