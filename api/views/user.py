from api.models import User, Picture, UserToken, Notification
from rest_framework import viewsets, permissions
from api.serializers import UserSerializer, PictureSerializer, UserTokenSerializer
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from json.decoder import JSONDecodeError
from sentry_sdk import capture_message
from datetime import datetime
from ..authentication import ExpiringTokenAuthentication, IsUserOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, action)
import json
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from ..utils import create_token, DEFAULT_IMAGE_URL, get_profile_image_id, send_registration_confirmation_mail, send_password_reset_mail


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    authentication_classes = (ExpiringTokenAuthentication,)
    # permission_classes = [IsAuthenticated, IsUserOrReadOnly]
    permission_classes = [IsUserOrReadOnly]
    serializer_class = UserSerializer
    http_method_names = ['get', 'patch', 'delete']

    def retrieve(self, request, pk):
        self.queryset = User.objects.all()
        # user = get_object_or_404(queryset, pk=pk)
        user = self.get_object()
        userData = self.serializer_class(user).data
        get_profile_image_id(userData, userData['id'])
        return Response(userData)


    def partial_update(self, request, pk, *args, **kwargs):
        self.queryset = User.objects.all()
        user = self.get_object()
        serializer = self.serializer_class(user, data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def user_login_response(serializer):
    userData = serializer.data
    get_profile_image_id(userData, userData['id'])
    token = serializer.get_token()
    token.created = timezone.now()
    token.save()
    userData["oauth_token"] = str(token.key)
    return {'status_code': 202, 'user': userData}


@csrf_exempt
@api_view(['POST'])
def login(request):
    data = json.loads(request.body)
    if ('email' in data.keys()) and ('password' in data.keys()):
        user = User.objects.filter(email=data['email'], deleted=False)
        if user:
            if user[0].register_status > 0:
                if user[0].check_password(data['password']):
                    user = user[0]
                    serializer = UserSerializer(user)
                    response = user_login_response(serializer)
                    return JsonResponse(response, status=202)
                return JsonResponse({'status_text': 'Contraseña incorrecta'}, status=403)
            return JsonResponse({'status_text': "El usuario no ha completado su validación de email"}, status=403)
        return JsonResponse({'status_text': "El usuario no existe"}, status=403)
    return JsonResponse({'status_text': "No se enviaron los parametros correctos"}, status=403)


@csrf_exempt
@api_view(['POST'])
def register(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError as error:
        return JsonResponse({'status_text': "Error parsing body: maybe a trailing comma?", 'error': str(error)},
                            status=400)
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        instance, token = serializer.save()
        userData = serializer.data
        token = str(token).replace("(<Token: ", "").replace(">, True)", "")
        userData["oauth_token"] = token
        response = {'status_code': 201, 'user': userData}
        capture_message(
            f'{datetime.now()}: {request.user} succesfully created')
        mail_token = create_token()
        data = {'token':mail_token, 'owner':userData['id'], 'validation': True}
        validation_token = UserTokenSerializer(data=data)
        if validation_token.is_valid():
            validation_token.save()
            try:
                send_registration_confirmation_mail(userData, validation_token.data)
                return JsonResponse({'status_text':'El mail de confirmacion fue enviado con exito'}, status=202)
            except:
                return JsonResponse({'status_text': "Ocurrio un error y el mail no pudo ser enviado"},
                                    status=400)
    return JsonResponse({'status_text': str(serializer.errors)}, status=400)

@csrf_exempt
@api_view(['POST'])
def register_mail_send(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError as error:
        return JsonResponse({'status_text': "Error parsing body: maybe a trailing comma?", 'error': str(error)},
                            status=400)
    try:
        user = User.objects.get(email = data['email'])
    except:
        return JsonResponse({'status_text': "Este mail no ha sido registrado con ningun usiario"},
                                status=400)
    if user.register_status == 0:
        token = UserToken.objects.filter(owner=user.id, validation=True)[0]
        try:
            send_registration_confirmation_mail(UserSerializer(user).data, UserTokenSerializer(token).data)
            return JsonResponse({'status_text':'El mail de confirmacion fue enviado con exito'}, status=202)
        except:
            return JsonResponse({'status_text': "Ocurrio un error y el mail no pudo ser enviado"},
                                status=400)
    else:
        return JsonResponse({'status_text': "Este usuario ya fue registrado con exito"},
                                status=400)



@csrf_exempt
@api_view(['POST'])
def register_confirmation(request):
    data = json.loads(request.body)
    response = 'No se envio el codigo'
    if 'register_token' in data.keys():
        print(UserToken.objects.filter(validation=True).filter(token=data['register_token']))
        token = UserToken.objects.filter(validation=True).filter(token=data['register_token'])[0]
        user = User.objects.get(email=token.owner)
        if user and token:
            serializer = UserSerializer(user, data={'register_status': 1}, partial = True)
            if serializer.is_valid():
                serializer.save()
                token.delete()
                return JsonResponse(serializer.data, status=202)
        else:
            return JsonResponse({'status_text': 'Codigo incorrecto'}, status=400)
    return JsonResponse({'status_text': response}, status=400)




@csrf_exempt
@api_view(['GET'])
@authentication_classes((ExpiringTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def loadUser(request):
    token = request.headers['Authorization'].replace("Token ", "")
    user = Token.objects.get(key=token).user
    if user:
        serializer = UserSerializer(user)
        userData = serializer.data
        userData["oauth_token"] = token
        get_profile_image_id(userData, userData['id'])
        response = {'status_code': 200, 'user': userData}
        return JsonResponse(response, status=200)
    return JsonResponse({'status_text': str(serializer.errors)}, status=400)

@csrf_exempt
@api_view(['GET'])
@authentication_classes((ExpiringTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def loadHeader(request):
    token = request.headers['Authorization'].replace("Token ", "")
    user = Token.objects.get(key=token).user.id
    if user:
        unread_notifications = False
        n_notifications = 0
        unread_messages = False
        n_messages = 0
        notifications = Notification.objects.filter(owner=user).filter(viewed=False)
        if len(notifications) > 0:
            unread_notifications = True
            n_notifications = len(notifications)
        response = {'unread_notifications': unread_notifications, 'n_notifications': n_notifications, 'unread_messages': unread_messages, 'n_messages': n_messages}
        return JsonResponse(response, status=200)
    return JsonResponse({'status_text': 'El token expiro'}, status=400)



@csrf_exempt
@api_view(['POST'])
@authentication_classes((ExpiringTokenAuthentication,))
@permission_classes((IsAuthenticated,))
def change_password(request):
    data = json.loads(request.body)
    response = 'Incorrect parameters'
    if ('new_password' in data.keys()) and ('password' in data.keys()):
        user = request.user
        response = 'Incorrect Password or Username'
        if user:
            if user.check_password(data['password']):
                user.set_password(data['new_password'])
                user.save()
                serializer = UserSerializer(user)
                response = user_login_response(serializer)
                return JsonResponse(response, status=202)

    return JsonResponse({'status_text': response}, status=400)


@csrf_exempt
@api_view(['POST'])
def reset_password(request):
    try:
        data = json.loads(request.body)
    except JSONDecodeError as error:
        return JsonResponse({'status_text': "Error parsing body: maybe a trailing comma?", 'error': str(error)},
                            status=400)
    email_reciever = data['email']
    try:
        user = User.objects.get(email = email_reciever)
    except:
        return JsonResponse({'status_text': 'No hay un usuario registrado con ese mail'}, status=404)
    mail_token = create_token()
    data = {'token':mail_token, 'owner':user.id, "recovery" : True}

    token = UserTokenSerializer(data=data)
    if token.is_valid():
        UserToken.objects.filter(owner=user.id).filter(recovery=True).delete()
        token.save()
    try:
        send_password_reset_mail(UserSerializer(user).data, token.data)
        return JsonResponse({'status_text':'El mail de confirmacion fue enviado con exito'}, status=202)
    except:
        return JsonResponse({'status_text': "Ocurrio un error y el mail no pudo ser enviado"},
                                status=400)

@csrf_exempt
@api_view(['POST'])
def change_password_recovery(request):
    data = json.loads(request.body)
    if ('new_password' in data.keys()) and ('password_token' in data.keys()):
        token = UserToken.objects.filter(recovery=True).filter(token=data['password_token'])
        print(token)
        if len(token) > 0:
            token = token[0]
            user = User.objects.get(id=token.owner.id)
            if user:
                user.set_password(data['new_password'])
                user.save()
                serializer = UserSerializer(user)
                response = user_login_response(serializer)
                token.delete()
                return JsonResponse(response, status=202)
        return JsonResponse({'status_text': 'Token incorrecto'}, status=400)
    return JsonResponse({'status_text': 'Parametros incorrectos'}, status=400)


@csrf_exempt
@api_view(['POST'])
def logout(request):
    return JsonResponse({}, status=202)

