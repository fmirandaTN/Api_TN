from random import randint
from .models import Notification, Picture, User, Proposal, Request, ProjectStage, ProjectJournal, Order
from .serializers import NotificationSerializer, UserSerializer, ProposalSerializer, ProjectStageSerializer, ProjectJournalSerializer, OrderSerializer
from re import search, sub
import os
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives


DEFAULT_IMAGE_URL = 'https://tenecesito-bucket.s3-us-west-1.amazonaws.com/profile-images/media/default_images/default{}.jpg'
RECOVERY_EMAIL_FORM = 'Estimado/a {}: \nRecibimos una solicitud para restablecer tu contraseña de Te Necesito. Ingresa al siguiente link para restablecerla:\n{}\n\n\n¿No solicitaste este cambio?\nSi no lo hiciste, ignora este mail y te recomendamos cambiar tu contraseña.'


def create_token():
    caracters = '0987654321asdfghjklpoiuytrewqzxcvbnm'
    token =''
    for caracter in range(25):
        token += str(caracters[randint(0,len(caracters) - 1)])

    return token

def censor_text(text):
    mail_patern = r'(\b[\w.]+@+[\w]+[.]+\w{1,3})'
    phone_patern = r'(\d{7,11})|(\+\d{3,11})|(\+\d{2,3}\s+\d{7,11})'
    out_text = sub(mail_patern, "*********", text)
    out_text = sub(phone_patern, "*********", out_text)
    return out_text

def send_notification(text_type, number_type, class_type, class_id, owner):
    notification_data = {'text_type' : text_type, 
                        'text_number': number_type,
                        'class_type' : class_type,
                        'class_id' : class_id, 
                        'owner' : owner}
    serializer = NotificationSerializer(data=notification_data)
    if serializer.is_valid():
        instance = serializer.save()
        return serializer.data
    else:
        print(serializer.errors)
        return 'Error'

def create_journal_entry(project_id, entry):
    entry_data = {'entry': entry,
                'project': project_id}
    serializer = ProjectJournalSerializer(data=entry_data)
    if serializer.is_valid():
        instance = serializer.save()
        return serializer.data
    else:
        print(serializer.errors)
        return 'Error'

def get_profile_image_notification(notification_list):
    for notification in notification_list:
        notification['image'] = DEFAULT_IMAGE_URL.format(1)

def get_profile_image_user(user_data, user):
    if user.id > 0:
        pic = Picture.objects.filter(owner=user.id)
        if len(pic) > 0:
            user_data['profile_image'] = pic[0].storage_url
        else:
            user_data['profile_image'] = DEFAULT_IMAGE_URL.format(user.default_image)
    else:
        user_data['profile_image'] = '-MINIMINIMI'

def get_profile_image_id(user_data, user_id):
    user = User.objects.get(id = user_id)
    return get_profile_image_user(user_data, user)

def add_user_data(data, user_id):
    user = UserSerializer(User.objects.get(id = user_id))
    data['user_data'] = user.data

def create_stages(proposal, project_id):
    proposal = ProposalSerializer(proposal).data
    for stage_index in range(len(proposal['stages'])):
        stage_dic ={"name":proposal['stages'][stage_index],
                    "price":proposal['prices'][stage_index],
                    "order": stage_index,
                    "project": project_id}
        serializer = ProjectStageSerializer(data = stage_dic)
        if serializer.is_valid():
            instance = serializer.save()

def add_progress_data(project_data):
    stages = ProjectStage.objects.filter(project=project_data['id'])
    journals = ProjectJournal.objects.filter(project=project_data['id'])
    project_data['stages'] = ProjectStageSerializer(stages, many=True).data
    project_data['journal'] = ProjectJournalSerializer(journals, many=True).data

def add_stages_data(project_data):
    stages = ProjectStage.objects.filter(project=project_data['id'])
    project_data['stages'] = ProjectStageSerializer(stages, many=True).data

ENV = 'dev'

if ENV == 'local':
    redirect_url = 'http://localhost:3000/#/'
elif ENV == 'dev':
    redirect_url = 'http://dev.tenecesito.cl/#/'
elif ENV == 'prod':
    pass

def send_registration_confirmation_mail(owner, token):
    email_reciever = owner['email']
    subject = '[Te Necesito] Confirmación de email'
    token_link = '{}registerConfirmation/?token={}'.format(redirect_url, token['token'])
    context = {'token':str(token['token']),
                'name': owner['first_name'] + ' ' + owner['last_name'],
                'link': token_link
            }
    email_body = render_to_string('register_confirmation_email.html', context)
    email_body_backup = strip_tags(email_body)
    msg = EmailMultiAlternatives(subject, email_body_backup, 'soporte@tenecesito.cl', [email_reciever])
    msg.attach_alternative(email_body, "text/html")
    msg.send()

def send_password_reset_mail(owner, token):
    print(owner)
    email_reciever = owner['email']
    subject = '[Te Necesito] Recuperación de Contraseña'
    token_link = '{}recoverPassword/?token={}'.format(redirect_url, token['token'])
    context = {'name': owner['first_name'] + ' ' + owner['last_name'],
                'link': token_link
            }
    email_body = render_to_string('password_reset_email.html', context)
    email_body_backup = strip_tags(email_body)
    msg = EmailMultiAlternatives(subject, email_body_backup, 'soporte@tenecesito.cl', [email_reciever])
    msg.attach_alternative(email_body, "text/html")
    msg.send()