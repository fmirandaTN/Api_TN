import tbk 
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from random import randint
from api.models import Order, LogTransbank, Project
from api.serializers import ProjectSerializer, OrderSerializer
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes, action)
from json.decoder import JSONDecodeError
import json
from ..utils import create_journal_entry, send_notification
from ..tbk_utils import TbkSettings, transaction_order, send_transaction_confirmation_mail
# import lxml.etree as ET


settings = TbkSettings()
webpay_service = tbk.services.WebpayService(settings.init_tbk())
transaction_order = transaction_order()

@csrf_exempt
@api_view(['POST'])
def initTransaction(request):
    settings = TbkSettings()
    try:
        data = json.loads(request.body)
    except JSONDecodeError as error:
        return JsonResponse({'status_text': "Error en el body del request", 'error': str(error)},
                            status=400)
    context = {}
    order = Order.objects.get(order_number=data['order_number'])
    
    return_url = "https://ten-backend-api.herokuapp.com"
    # return_url = "http://localhost:3000"
    transaction = webpay_service.init_transaction(
            amount=int(order.gross_payment),
    	    buy_order=int(order.order_number),
    	    # return_url=settings.get_base_url() + "/tbkNormal/",
            return_url= return_url + "/tbkNormal/",
    	    # final_url=settings.get_base_url() + "/tbkNormal/",
    	    final_url= return_url + "/tbkFinal/",
    	    session_id= randint(100, 1000)
    	)
    print(transaction)
    context['transaction'] = transaction
    out_dic = {'token': transaction['token'],
                'url': transaction['url']}
    print(context)
    transaction_order.set_mount(order.gross_payment)
    transaction_order.set_id_order(data['order_number'])
    transaction_order.set_token(transaction['token'])
    return Response(out_dic, status=status.HTTP_202_ACCEPTED)


# redirect_link = "http://prueba.tenecesito.cl/#/viewProject/{}"
redirect_link = "http://localhost:3000/#/viewProject/{}"

@csrf_exempt
@api_view(['POST'])
def normal_return_webpay(request):
    token = request.POST.get('token_ws')
    transaction = webpay_service.get_transaction_result(token)
    transaction_details = transaction['detailOutput'][0]
    webpay_service.acknowledge_transaction(token)
    order = Order.objects.get(order_number = transaction['buyOrder'])
    context = {}
    # if transaction_details['responseCode'] == 0 and token == transaction_order.get_token():
    if transaction_details['responseCode'] == 0:
        template_name = 'success_normal.html'
        transaction_order.set_cardNumber(transaction['cardDetail']['cardNumber'])
        transaction_order.set_authorizationCode(transaction_details['authorizationCode'])
        transaction_order.set_paymentTypeCode(transaction_details['paymentTypeCode'])

        create_journal_entry(order.project.id, 3)
        serializer_o = OrderSerializer(order, data={'paid': True}, partial = True)
        if serializer_o.is_valid():
            serializer_o.save()
        context['transaction'] = transaction

        log = LogTransbank.objects.create(order=order,
                            authorization_code=transaction_details['authorizationCode'],
                            token=token,
                            card_number=transaction['cardDetail']['cardNumber'],
                            gross_payment=order.gross_payment)

        project = Project.objects.get(id=order.project.id)
        serializer = ProjectSerializer(project, data={'status': 'in_progress'}, partial = True)
        if serializer.is_valid():
            serializer.save()

        if len(transaction_details) != 0:
            context['transaction_detail'] = transaction_details
        context['token'] = token
        context['order'] = order
        send_notification('request-collaborator', 7, 'project', order.project.id, order.project.collaborator_id)
        send_transaction_confirmation_mail(order.project.owner.id, order.project, order)
        return render(request, template_name, context)
        # return Response(context, status=status.HTTP_202_ACCEPTED)
    else:
        context['transaction'] = transaction
        template_name = 'failure_normal.html'
        if len(transaction_details) != 0:
            context['transaction_detail'] = transaction_details
        context['token'] = token
        context['redirect_link'] = redirect_link.format(order.project.id)
        return render(request, template_name, context)
        # return JsonResponse({'status_text': "Fallo la transacccion"},
        #                 status=400)

@csrf_exempt
@api_view(['POST'])
def normal_final(request):
    template_name = 'final_normal.html'
    context = {}
    token = request.POST.get('token_ws')
    context['token'] = token
    log = LogTransbank.objects.filter(token = token)[0]
    context['redirect_link'] = redirect_link.format(log.order.project.id)
    return render(request, template_name, context)

@api_view(['GET'])
def testing(request):
    template_name = 'success_normal.html'
    context = {'transaction_detail':{'plata': 500, 'orden':2132322323, 'fecha': '22/22/1995'}}
    print(context)
    return render(request, template_name, context)