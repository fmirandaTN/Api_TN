from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase, APIClient, RequestsClient
from api.models import User
import json
from rest_framework import status
from rest_framework.authtoken.models import Token
from api.serializers import UserSerializer

factory = APIRequestFactory()
client1 = RequestsClient()
client2 = APIClient()


class UserTestCase(APITestCase):
    """Test para el modelo User"""

    def setUp(self):
        self.url = '/users/'
        self.register_url = '/api/auth/register'
        self.login_url = '/login/'
        self.loaduser_url = '/loadUser/'
        self.change_password_url = '/changePassword/'

        """Primero registramos 2 nuevos usuarios"""

        self.user_rcuevas = User.objects.create(first_name="Robin", last_name="Cuevas",
                                                   username="rcuevas", email="rcuevas@tenecesito.cl", password="123456")
        self.token_rcuevas = Token.objects.create(user=self.user_rcuevas)
        self.header_rcuevas = "Token {}".format(self.token_rcuevas)
        self.id_rcuevas = self.user_rcuevas.id

        self.user_famigol = User.objects.create(first_name="Felipe", last_name="Amigo",
                                                   username="famigol", email="famigo@tenecesito.cl", password="123456")
        self.token_famigol = Token.objects.create(user=self.user_famigol)
        self.header_famigol = "Token {}".format(self.token_famigol)

    def testRegisterUser(self):
        "Registramos un usuario"

        json_data = json.dumps({"first_name": "Joaco",
                                "last_name": "Molina",
                                "username": "jmolina",
                                "email": "jmolina@tenecesito.cl",
                                "password": "123456",
                                })
        response = self.client.post(self.register_url,
                                    json_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testLoginUser(self):
        """Registramos a un usuario e iniciamos sesion"""

        json_data = json.dumps({"first_name": "Raimundo",
                                "last_name": "Molina",
                                "username": "rmolina",
                                "email": "rmolina@tenecesito.cl",
                                "password": "123456",
                                })
        response = self.client.post(self.register_url,
                                    json_data,
                                    content_type="application/json")

        response2 = self.client.post(self.login_url,
                                     json.dumps({'email': 'rmolina@tenecesito.cl',
                                                 'password': '123456',
                                                 }),
                                     content_type="application/json")
                                     
        self.assertEqual(response2.status_code, status.HTTP_202_ACCEPTED)

    def testLoadUserUser(self):
        "Cargamos un usuario con su token"

        response = self.client.get(f'/loadUser/',
                                   **{'HTTP_AUTHORIZATION': self.header_rcuevas})
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)

    def testRepeatingEmail(self):
        "No se puede crear un usuario con un mail existente"

        json_data = json.dumps({"first_name": "Robin",
                                "last_name": "Cuevas",
                                "username": "robincuevas",
                                "email": "rcuevas@tenecesito.cl",
                                "password": "123456",
                                })
        response = self.client.post(self.register_url,
                                    json_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        
    def testRepeatingUsername(self):
        "No se puede crear un usuario con un usuario existente"

        json_data = json.dumps({"first_name": "Robin",
                                "last_name": "Cuevas",
                                "username": "rcuevas",
                                "email": "Elrobin@tenecesito.cl",
                                "password": "123456",
                                })
        response = self.client.post(self.register_url,
                                    json_data,
                                    content_type="application/json")
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def testPatchUserself(self):
        "Se puede editar un usuario"

        json_data = json.dumps({"default_image": 2,
                                "about_me": "estudiante",
                                "experience" : "Sin experiencia",
                                "may_interested" : "deportes acuaticos",
                                "profession": "Ingeniero Civil"
                                })
        response = self.client.patch(self.url + '{}/'.format(self.id_rcuevas),
                                    json_data,
                                    content_type="application/json",
                                     **{'HTTP_AUTHORIZATION': self.header_rcuevas})

        self.assertEqual(response.status_code,
                         status.HTTP_202_ACCEPTED)

        userresponse = self.client.get(self.url + '{}/'.format(self.id_rcuevas),
                                    content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self.header_rcuevas})
        self.assertEqual(userresponse.data['profession'],
                         "Ingeniero Civil")
        self.assertEqual(userresponse.data['experience'],
                         "Sin experiencia")
        self.assertEqual(userresponse.data['default_image'],
                         2)


    def testPatchPermissionsDenied(self):
        "Ne puede editar un usuario sin su token e iniciado sesion"

        json_data = json.dumps({"default_image": 2,
                                "about_me": "estudiante",
                                "experience" : "Sin experiencia",
                                "may_interested" : "deportes acuaticos",
                                "profession": "Ingeniero Civil"
                                })
        response = self.client.patch(self.url + '{}/'.format(self.id_rcuevas),
                                    json_data,
                                    content_type="application/json",
                                     **{'HTTP_AUTHORIZATION': self.header_famigol})

        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)

        userresponse = self.client.get(self.url + '{}/'.format(self.id_rcuevas),
                                    content_type="application/json",
                                    **{'HTTP_AUTHORIZATION': self.header_famigol})

        self.assertNotEqual(userresponse.data['profession'],
                         "Ingeniero Civil")
        self.assertNotEqual(userresponse.data['experience'],
                         "Sin experiencia")
        self.assertNotEqual(userresponse.data['default_image'],
                         2)

    def testChangePassword(self):
        "Se puede cambiar de contraseña e iniciar sesion"

        json_data = json.dumps({"first_name": "Joaco",
                                "last_name": "Molina",
                                "username": "jmolina",
                                "email": "jmolina@tenecesito.cl",
                                "password": "123456",
                                })
        user = self.client.post(self.register_url,
                        json_data,
                        content_type="application/json")
        token = json.loads(user.content)['user']['oauth_token']

        json_data = json.dumps({"password": "123456",
                                "new_password": "654321"
                                })
        response = self.client.post(self.change_password_url,
                                    json_data,
                                    content_type="application/json",
                                    **{'HTTP_AUTHORIZATION':'Token {}'.format(token)}
                                    )

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)  
        response1 = self.client.post(self.login_url,
                                     json.dumps({'email': 'jmolina@tenecesito.cl',
                                                 'password': '123456',
                                                 }),
                                     content_type="application/json")
                                     
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

        response2 = self.client.post(self.login_url,
                                     json.dumps({'email': 'jmolina@tenecesito.cl',
                                                 'password': '654321',
                                                 }),
                                     content_type="application/json")
                                     
        self.assertEqual(response2.status_code, status.HTTP_202_ACCEPTED)

    
    