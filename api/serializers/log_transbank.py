from rest_framework import serializers
from api.models import LogTransbank

class LogTransbankSerializer(serializers.ModelSerializer):

    class Meta:
        model = LogTransbank
        fields = ('id', 'gross_payment', 'order', 'token', 'card_number', 'authorization_code')
        read_only_fields = ('created_at',) 