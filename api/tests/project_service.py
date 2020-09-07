from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from api.models import Project, User, Service
import json
from rest_framework import status


class ProjectTestCase(APITestCase):

    def setUp(self):

        """Creamos 2 usuarios"""
        self.url = '/projects/'
        self.register = '/registerProject/'
        self.get_id = '/projects/{}/'
        self.get_owner = '/projects/?owner={}'
        self.get_status = '/projects/?status={}'
        self.get_category = '/projects/?category={}'
        self.get_subcategory = '/projects/?subcategory={}'

        self.user_fjsalinas = User.objects.create(first_name="Fernando", last_name="Salinas",
                                                  username="fjsalinas", email="fjsalinas@tenecesito.cl")
        self.user_fjsalinas.set_password("123456")
        self.user_fjsalinas.save()
        self.token_fjsalinas = Token.objects.create(user=self.user_fjsalinas)
        self.header_fjsalinas = 'Token {}'.format(self.token_fjsalinas)
        self.id_fjsalinas = self.user_fjsalinas.id

        self.user_fjherrera = User.objects.create(first_name="Francisco", last_name="Herrera",
                                                  username="fjherrera", email="fjherrera@tenecesito.cl")
        self.user_fjherrera.set_password("123456")
        self.user_fjherrera.save()
        self.token_fjherrera = Token.objects.create(user=self.user_fjherrera)
        self.header_fjherrera = 'Token {}'.format(self.token_fjherrera)
        self.id_fjherrera = self.user_fjherrera.id

        self.project = Project.objects.create(
            # owner=self.id_fjsalinas,
            owner=self.user_fjsalinas,
            title='Titulo Proyecto de Prueba',
            description="Descripcion del Proyecto de prueba",
            skills_required=list(['Python', 'React']),
            categories=list(['Postgresql']),
            work_modality="mixed",
            min_price_range=100000,
            max_price_range=120000
        )

        self.new_project_data = {
                                    "title": "Necesito encargado de base de datos",
                                    "description": "Se busca una persona que se maneje con basesde datos en postgresql para poder obtener datos para tomar desiciones estrategicas",
                                    "categories": ["Programación"],
                                    "skills_required": ["Postgresql"],
                                    "owner": self.id_fjherrera,
                                    "min_price_range": 1000000,
                                    "max_price_range": 2000000,
                                    "work_modality": "mixed"
                                }

        self.new_project_data2 = {
                                    "title": "Desarrollo pagina web",
                                    "description": "Estamos creando una nueva tienda de alimento para mascotas y necesitamos a alguien que nos haga una pagina web que facilite nuestras ventas",
                                    "categories": ["Programación"],
                                    "skills_required": ["Javascript"],
                                    "owner": self.id_fjherrera,
                                    "min_price_range": 700000,
                                    "max_price_range": 1300000,
                                    "work_modality": "parttime",
                                    "status": "in_progress",
                                    "collaborator_id": self.id_fjsalinas
                                }
        self.patch_data = { "status": "in_progress",
                            "experience_required": "Cierta experiencia",
                            "collaborator_id": self.id_fjherrera,
                            "title": "Prueba"
                            }

    def testRegisterProject(self):
        
        response = self.client.post(self.register, self.new_project_data,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': self.header_fjsalinas})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def testPatchProject(self):

        response = self.client.patch(self.get_id.format(self.project.id), self.patch_data,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': self.header_fjsalinas})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['status'],
                         self.patch_data['status'])
        self.assertEqual(response.data['experience_required'],
                         self.patch_data['experience_required'])
        self.assertEqual(response.data['title'],
                         self.patch_data['title'])

    def testPatchProjectUnauthorized(self):

        response = self.client.patch(self.get_id.format(self.project.id), self.patch_data,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': self.header_fjherrera})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def testGetProjectOwner(self):
        
        response = self.client.get(self.get_owner.format(self.id_fjsalinas),
                                    format='json')
        self.assertEqual(response.data['total_objects'], 1)

        response = self.client.get(self.get_owner.format(self.id_fjherrera),
                                    format='json')
        
        self.assertEqual(response.data['total_objects'], 0)


    def testGetProjectStatus(self):

        
        response = self.client.get(self.get_status.format("published"),
                                    format='json')
        self.assertEqual(response.data['total_objects'], 1)
        response = self.client.get(self.get_status.format("in_progress"),
                                    format='json')
        self.assertEqual(response.data['total_objects'], 0)


    def testGetProjectCategory(self):
        response = self.client.get(self.get_category.format("Postgresql"),
                                    format='json')
        self.assertEqual(response.data['total_objects'], 1)
        response = self.client.get(self.get_category.format("Computacion"),
                                    format='json')
        self.assertEqual(response.data['total_objects'], 0)


    def testDeleteProject(self):
        pass

class ServiceTestCase(APITestCase):

    def setUp(self):
               
        """Creamos 2 usuarios"""
        self.url = '/services/'
        self.register = '/registerService/'
        self.get_id = '/services/{}/'
        self.get_owner = '/services/?owner={}'
        self.get_status = '/services/?status={}'
        self.get_category = '/services/?category={}'
        self.get_subcategory = '/services/?subcategory={}'

        self.user_fjsalinas = User.objects.create(first_name="Fernando", last_name="Salinas",
                                                  username="fjsalinas", email="fjsalinas@tenecesito.cl")
        self.user_fjsalinas.set_password("123456")
        self.user_fjsalinas.save()
        self.token_fjsalinas = Token.objects.create(user=self.user_fjsalinas)
        self.header_fjsalinas = 'Token {}'.format(self.token_fjsalinas)
        self.id_fjsalinas = self.user_fjsalinas.id

        self.user_fjherrera = User.objects.create(first_name="Francisco", last_name="Herrera",
                                                  username="fjherrera", email="fjherrera@tenecesito.cl")
        self.user_fjherrera.set_password("123456")
        self.user_fjherrera.save()
        self.token_fjherrera = Token.objects.create(user=self.user_fjherrera)
        self.header_fjherrera = 'Token {}'.format(self.token_fjherrera)
        self.id_fjherrera = self.user_fjherrera.id

        self.service = Service.objects.create(owner=self.user_fjsalinas,
                                                title="Desarrollador Web",
                                                description="Poseo un gran manejo en el desarrollo de plataformas web de todo tipo",
                                                experience= "Recientemente desarrolle la pagina web de la pyme Chocolatoso SA (www.chocolatoso.cl)",
                                                categories=list(["TI y Software"]),
                                                work_modality="mixed",
                                                availability="Lunes a sabado",
                                                min_price_range=100000,
                                                max_price_range=120000)

        self.new_service_data = {"title": "Servicios de contador",
                                    "description": "Soy un contador con 10 años de experiencia, estoy dispuesto a asistr a cualquier empresa en sus temas de contabilidad y de libro mayor",
                                    "experience": "Certificado por la CONTACH",
                                    "owner": self.id_fjsalinas,
                                    "categories": ["Contabilidad y Finanzas"],
                                    "min_price_range": 800000,
                                    "max_price_range": 2500000,
                                    "work_modality": "parttime",
                                    "created_at": "2020-06-11T15:16:48.290Z",
                                    "updated_at":"2020-06-11T15:16:48.290Z",
                                    "availability": "Lunes, martes y jueves"
                                }

                                
        self.patch_data = { "status": "inactive",
                            "experience": "Certificado por la INACH",
                            "title": "Prueba",
                            "work_modality":"parttime"
                            }

    def testRegisterService(self):
        response = self.client.post(self.register, self.new_service_data,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': self.header_fjsalinas})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def testPatchService(self):
        response = self.client.patch(self.get_id.format(self.service.id), self.patch_data,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': self.header_fjsalinas})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['status'],
                         self.patch_data['status'])
        self.assertEqual(response.data['experience'],
                         self.patch_data['experience'])
        self.assertEqual(response.data['title'],
                         self.patch_data['title'])

    def testPatchServiceUnauthorized(self):
        response = self.client.patch(self.get_id.format(self.service.id), self.patch_data,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': self.header_fjherrera})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def testGetServiceOwner(self):
        response = self.client.get(self.get_owner.format(self.id_fjsalinas),
                                    format='json')
        self.assertEqual(response.data['total_objects'], 1)

        response = self.client.get(self.get_owner.format(self.id_fjherrera),
                                    format='json')
        
        self.assertEqual(response.data['total_objects'], 0)

    def testGetServiceStatus(self):
        response = self.client.get(self.get_status.format("active"),
                                    format='json')
        self.assertEqual(response.data['total_objects'], 1)
        response = self.client.get(self.get_status.format("inactive"),
                                    format='json')
        self.assertEqual(response.data['total_objects'], 0)

    def testGetServiceCategory(self):
        response = self.client.get(self.get_category.format("TI y Software"),
                            format='json')
        self.assertEqual(response.data['total_objects'], 1)
        response = self.client.get(self.get_category.format("Computacion"),
                                    format='json')
        self.assertEqual(response.data['total_objects'], 0)

    def testDeleteService(self):
        pass
