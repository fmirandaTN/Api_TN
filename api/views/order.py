from api.models import Order
from rest_framework import viewsets, permissions
from api.serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from json.decoder import JSONDecodeError
import json
from django.http.response import JsonResponse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, action)
from ..authentication import ExpiringTokenAuthentication, IsEmitterOrReadOnlyProposal
from rest_framework.permissions import IsAuthenticated



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    # def get_queryset(self):
    #     self.queryset = Order.objects.all()
    #     order = self.queryset
    #     if 'project' in self.request.query_params.keys():
    #         order = Proposal.objects.filter(request=self.request.query_params['request']).order_by('created_at')
    #     return order

    # def list(self, request):
    #     queryset = self.get_queryset()
    #     list_data = ProposalSerializer(queryset, many=True).data
    #     for proposal in list_data:
    #         stages_dic = {}
    #         stgs = proposal['stages']
    #         prices = proposal['prices']
    #         for s in range(len(proposal['stages'])):
    #             stages_dic[stgs[s]]= prices[s]
    #         proposal['stages'] = stages_dic
    #         del proposal['prices']
    #     return Response(list_data, status=status.HTTP_200_OK)

    # def retrieve(self, request, pk):
    #     queryset = Proposal.objects.all()
    #     proposal = self.get_object()
    #     proposal = ProposalSerializer(proposal).data
    #     stages_dic = {}
    #     stgs = proposal['stages']
    #     prices = proposal['prices']
    #     for s in range(len(proposal['stages'])):
    #         stages_dic[stgs[s]]= prices[s]
    #     proposal['stages'] = stages_dic
    #     del proposal['prices']
    #     return Response(proposal, status=status.HTTP_200_OK)


    def create(self, request):
        try:
            data = json.loads(request.body)
        except JSONDecodeError as error:
            return JsonResponse({'Proposal error': str(error)},
                                status=400)

        serializer = self.serializer_class(data = data)
        if serializer.is_valid():
            instance = serializer.save()
            orderData = serializer.data
            response = {'status_code': 201, 'order': orderData}
            return JsonResponse(response, status=201)
        return JsonResponse({'status_text': str(serializer.errors)}, status=400)