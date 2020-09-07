from random import randint
from .models import Proposal, Order, User
from .serializers import ProposalSerializer, OrderSerializer
import os
import tbk
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail, EmailMultiAlternatives




class TbkSettings():
    CERTIFICATES_DIR = os.path.join(os.path.dirname(__file__), 'commerces')
    ENV = 'dev'

    if ENV == 'local':
        redirect_url = 'http://localhost:8000/'
    elif ENV == 'dev':
        redirect_url = "https://ten-backend-api.herokuapp.com"
    elif ENV == 'prod':
        pass

    # Local credentials
    # HOST = os.getenv('HOST', 'http://127.0.0.1')
    # PORT = os.getenv('PORT', '8000')
    HOST = os.getenv('HOST', 'http://localhost')
    PORT = os.getenv('PORT', '3000')
    # http://localhost:3000/#/tbkNormal
    BASE_URL = '{host}:{port}'.format(host=HOST, port=PORT)
    # Test credentials
    # HOST = os.getenv('HOST', '')
    # BASE_URL = '{host}'.format(host=HOST)

    NORMAL_COMMERCE_CODE = ""

    def load_commerce_data(self, commerce_code):
        with open(os.path.join(self.CERTIFICATES_DIR, commerce_code, commerce_code + '.key'), 'r') as file:
            key_data = file.read()
        with open(os.path.join(self.CERTIFICATES_DIR, commerce_code, commerce_code + '.crt'), 'r') as file:
            cert_data = file.read()
        with open(os.path.join(self.CERTIFICATES_DIR, 'tbk.pem'), 'r') as file:
            tbk_cert_data = file.read() 
        return {
            'key_data': key_data,
            'cert_data': cert_data,
            'tbk_cert_data': tbk_cert_data}

    def init_tbk(self):
        self.NORMAL_COMMERCE_CODE = "597020000541"
        normal_commerce_data = self.load_commerce_data(self.NORMAL_COMMERCE_CODE)
        normal_commerce = tbk.commerce.Commerce(
            commerce_code= self.NORMAL_COMMERCE_CODE,
            key_data= normal_commerce_data['key_data'],
            cert_data= normal_commerce_data['cert_data'],
            tbk_cert_data= normal_commerce_data['tbk_cert_data'],
            environment = tbk.environments.DEVELOPMENT
        )
        return normal_commerce

    def get_base_url(self):
        return self.BASE_URL

class transaction_order:
    id_order = 0
    mount = 0
    token = ''
    authorizationCode = ''
    paymentTypeCode = ''
    cardNumber = ''

    def get_id_order(self, token):
        if str(token) == self.token:
            return self.id_order
        else:
            return 'Invalid Token'

    def get_mount(self, token):
        if str(token) == self.token:
            return self.mount
        else:
            return 'Invalid Token'

    def get_token(self):
        return self.token

    def get_authorizationCode(self):
        return self.authorizationCode

    def get_cardNumber(self):
        return self.cardNumber

    def get_paymentTypeCode(self):
        return self.paymentTypeCode


    def set_token(self, token):
        self.token = token

    def set_authorizationCode(self, code):
        self.authorizationCode = code

    def set_cardNumber(self, cardNumber):
        self.cardNumber = cardNumber

    def set_paymentTypeCode(self, paymentTypeCode):
        self.paymentTypeCode = paymentTypeCode

    def set_mount(self, mount):
        self.cardNumber = mount

    def set_token(self, token):
        self.token = token

    def set_id_order(self, id_order):
        self.id_order = id_order


def create_payment_order(proposal, project_id):
    proposal = ProposalSerializer(proposal).data
    order_dic ={"payment_type": "TBK",
                "gross_payment":proposal['total_price'],
                "order": project_id,
                "project": project_id}
    serializer = OrderSerializer(data = order_dic)
    if serializer.is_valid():
        instance = serializer.save()
	

CONFIRMATION_EMAIL_FORM = 'Hola {}\nEl pago de tu proyecto {} fue completado correctamente.\n \n DETALLES DEL PEDIDO\n \n - Pedido: {}\n \n - Fecha de Pago: {}\n \n - Pago: Webpay \n \n - Monto + IVA: {} \n \n Puede revisar su factura en los proximos días en la pestaña \'Cuentas Claras\' de su perfil. \n Saludo de Te Necesito team.'
def send_transaction_confirmation_mail(owner_id, project, order):
    user = User.objects.get(id=owner_id)
    email_reciever = user.email
    print(email_reciever)
    subject = '[Te Necesito] Confirmación de Pago del Proyecto'
    context = {'order_number':str(order.order_number),
                'name': user.first_name + ' ' + user.last_name,
                'date': order.created_at,
                'gross_payment':str(order.gross_payment),
                'type_payment': 'Webpay',
                'project_title': project.title}
    email_body = CONFIRMATION_EMAIL_FORM.format(user.first_name + ' ' + user.last_name, project.title, str(order.order_number), order.created_at, str(order.gross_payment))
    email_body2 = render_to_string('payment_confirmation_email.html', context)
    email_body3 = strip_tags(email_body2)
    msg = EmailMultiAlternatives(subject, email_body3, 'soporte@tenecesito.cl', [email_reciever])
    msg.attach_alternative(email_body2, "text/html")
    msg.send()