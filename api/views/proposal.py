from api.models import Proposal, Project, Request
from rest_framework import viewsets, permissions
from api.serializers import ProposalSerializer, ProjectSerializer, RequestSerializer
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
from ..utils import send_notification, censor_text

def model_to_view(proposalData):
    stages = []
    for index in range(len(proposalData['stages'])):
        stages.append({"name":proposalData['stages'][index], "price":proposalData['prices'][index]})
    proposalData['stages'] = stages
    del proposalData['prices']
    return proposalData

class ProposalViewSet(viewsets.ModelViewSet):
    queryset = Proposal.objects.all()
    serializer_class = ProposalSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = [IsEmitterOrReadOnlyProposal & IsAuthenticated]
    http_method_names = ['get', 'patch', 'delete', 'post']
     
    def get_queryset(self):
        self.queryset = Proposal.objects.all()
        proposals = self.queryset
        if 'request' in self.request.query_params.keys():
            proposals = Proposal.objects.filter(request=self.request.query_params['request']).order_by('created_at')
        if 'last' in self.request.query_params.keys():
            proposals = proposals.order_by('created_at').reverse()[0]
        return proposals

    def list(self, request):
        queryset = self.get_queryset()
        list_data = ProposalSerializer(queryset, many=True).data
        new_list = []
        for proposal in list_data:
            new_list.append(model_to_view(proposal))
        return Response(new_list, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        queryset = Proposal.objects.all()
        proposal = self.get_object()
        proposal = ProposalSerializer(proposal).data
        new_proposal = model_to_view(proposal)
        return Response(new_proposal, status=status.HTTP_200_OK)

        
    def create(self, request):
        try:
            data = json.loads(request.body)
        except JSONDecodeError as error:
            return JsonResponse({'Proposal error': str(error)},
                                status=400)
        original_list = list(data['stages'])
        stages = []
        prices = []
        for stage in data['stages']:
            stages.append(stage['name'])
            prices.append(stage['price'])
        data['stages'] = stages
        data['prices'] = prices
        data.pop("total_price", None)
        data['text'] = censor_text(data['text'])
        request = Request.objects.get(id = data['request'])
        if request:
            serializer = ProposalSerializer(data = data)
            if serializer.is_valid():
                accepted_proposal = Proposal.objects.filter(request=request.id).filter(accepted=True)
                if len(accepted_proposal) > 0:
                    unaccept = self.serializer_class(accepted_proposal[0], data={"accepted": False}, partial = True)
                    if unaccept.is_valid():
                        unaccept.save()
                serializer.save()
                if data['emitter'] == request.project.owner:
                    send_notification('request-collaborator', 3, 'request', data['request'], request.emitter.id)
                elif data['emitter'] == request.emitter:
                    send_notification('project', 2, 'request', data['request'], request.project.owner)
                proposalData = serializer.data
                proposalData['stages'] = original_list
                del proposalData['prices']
                
                response = {'status_code': 201, 'proposal': proposalData}
                return JsonResponse(response, status=201)
            return JsonResponse({'status_text': str(serializer.errors)}, status=400)
        else:
            return JsonResponse({'status_text': "El proyecto no existe!"},
                            status=400)

    def partial_update(self, request, *args, **kwargs):
        self.queryset = Proposal.objects.all()
        proposal = self.get_object()
        if 'accepted' in request.data.keys():
            if request.data['accepted'] == True:
                proposals = Proposal.objects.filter(request=proposal.request.id).filter(accepted=True)
                if len(proposals) < 1:
                    recent = Proposal.objects.filter(request=proposal.request.id).order_by('created_at').reverse()
                    if recent[0] == proposal:
                        serializer = self.serializer_class(proposal, data={"accepted": True}, partial = True)
                        if serializer.is_valid():
                            serializer.save()
                            proposal_data = serializer.data
                            if proposal.emitter == proposal.request.emitter:
                                send_notification('project', 5 , 'request', proposal.request.id, proposal.request.project.owner.id)
                            elif proposal.emitter == proposal.request.project.owner:
                                # send_notification('request-collaborator', 4 , 'request', proposal.request.id, proposal.request.emitter.id)
                                send_notification('request-collaborator', 4 , 'project', proposal.request.project.id, proposal.request.emitter.id)
                            return Response(model_to_view(proposal_data), status=status.HTTP_202_ACCEPTED)
                        else:
                            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                    return JsonResponse({'status_test': "Solo se puede aceptar la ultima negociación"},
                    status=400)
                return JsonResponse({'status_test': "No se puede aceptar más de una negociación."},
                    status=400)
        return JsonResponse({'status_test': "No se puede editar los otros campos de la negociación."},
                    status=400)
