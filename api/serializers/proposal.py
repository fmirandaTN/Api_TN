from rest_framework import serializers
from api.models import Proposal


class ProposalSerializer(serializers.ModelSerializer):
    total_price = serializers.IntegerField(required=False)

    class Meta:
        model = Proposal
        fields = ('id', 'stages', 'prices', 'request', 'emitter', 'accepted', 'text', 'total_price',
                    'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')