from api.models import KbCard
from rest_framework import viewsets
from api.serializers import KbCardSerializer
from django.http.response import JsonResponse
from json.decoder import JSONDecodeError
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, action)
from ..authentication import ExpiringTokenAuthentication, IsOwnerOrReadOnly, ProjectStatus
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated


class KbCardViewSet(viewsets.ModelViewSet):
    queryset = KbCard.objects.all()
    serializer_class = KbCardSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    # permission_classes = [IsOwnerOrReadOnly, ProjectStatus, IsAuthenticatedOrReadOnly]
    http_method_names = ['get']

    def get_queryset(self):
        self.queryset = KbCard.objects.all()
        cards = self.queryset
        if self.request.query_params.keys():
            if 'project' in self.request.query_params.keys():
                project = int(self.request.query_params['project'])
                cards= cards.filter(project=project).order_by('position')
        return cards


@csrf_exempt
@api_view(['POST'])
def changeBoard(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError as error:
        return JsonResponse({'status_text': "Error en el body del request", 'error': str(error)},
                            status=400)
    print(data)
    card_list = []
    try:
        if 'CREATE' in data.keys():
            for card in data['CREATE']:
                serializer = KbCardSerializer(data=card)
                if serializer.is_valid():
                    instance = serializer.save()
                    card_list.append(serializer.data)
                else:
                     return JsonResponse({'status_text': str(serializer.errors)}, status=400)

        if 'UPDATE' in data.keys():
            for cardData in data['UPDATE']:
                print(cardData)
                card = KbCard.objects.get(id=cardData['id'])
                serializer = KbCardSerializer(card, data=cardData, partial = True)
                if serializer.is_valid():
                    serializer.save()
                    card_list.append(serializer.data)
                else:
                     return JsonResponse({'status_text': str(serializer.errors)}, status=400)

        if 'DELETE' in data.keys():
            for card in data['DELETE']:
                card = KbCard.objects.get(id=card['id']).delete()

        response = {'status_code': 201, 'cards': card_list}
        return JsonResponse(response, status=201)
    except:
        return JsonResponse({'status_text': "Error decoding"}, status=400)
   