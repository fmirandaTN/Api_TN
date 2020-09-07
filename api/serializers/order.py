from rest_framework import serializers
from api.models import Order

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('id', 'gross_payment', 'order_number', 'payment_type', 'project', 'paid')
        read_only_fields = ('created_at',) 
