from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from api.models import Project, User, Request, Rating
import json
from rest_framework import status


class RatingTestCase(APITestCase):

    def setUp(self):
        self.url = '/ratings/'
        self.get_id = '/ratings/{}/'
        self.get_ratingtype = '/ratings/?rating_type={}&user_id={}'
        self.get_project = '/ratings/?project={}'

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

        self.user_rcuevas = User.objects.create(first_name="Robin", last_name="Cuevas",
                                                   username="rcuevas", email="rcuevas@tenecesito.cl", password="123456")
        self.user_rcuevas.set_password("123456")
        self.user_rcuevas.save()
        self.token_rcuevas = Token.objects.create(user=self.user_rcuevas)
        self.header_rcuevas = "Token {}".format(self.token_rcuevas)
        self.id_rcuevas = self.user_rcuevas.id

        self.project = Project.objects.create(
            owner=self.user_fjsalinas,
            title='Titulo Proyecto de Prueba',
            description="Descripcion del Proyecto de prueba",
            skills_required=list(['Python', 'React']),
            categories=list(['Postgresql']),
            work_modality="mixed",
            min_price_range=100000,
            max_price_range=120000,
            status="completed",
            collaborator_id=self.id_fjherrera
        )
        self.project2 = Project.objects.create(
            owner=self.user_fjsalinas,
            title='Titulo Proyecto de Prueba2',
            description="Descripcion del Proyecto de prueba",
            skills_required=list(['Python', 'React']),
            categories=list(['Postgresql']),
            work_modality="mixed",
            min_price_range=100000,
            max_price_range=120000,
            status="in_progress",
            collaborator_id=self.id_fjherrera
            )
        self.rating = Rating.objects.create(
            rating=5,
            rating_type="collaborator",
            project=self.project
            )
        self.new_rating_data = {
            "rating":2,
            "rating_type":"client",
            "project": self.project.id
        }
        self.new_rating_data2 = {
            "rating":2,
            "rating_type":"collaborator",
            "project": self.project.id
        }
        self.new_rating_data3 = {
            "rating":2,
            "rating_type":"client",
            "project": self.project2.id
        }


    def testCreateRating(self):

        response = self.client.post(self.url, self.new_rating_data,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': self.header_fjsalinas})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testCreateRatingProjectNotCompleted(self):

        response = self.client.post(self.url, self.new_rating_data3,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': self.header_fjsalinas})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCreateRatingUserAlreadyCreated(self):

        response = self.client.post(self.url, self.new_rating_data2,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': self.header_fjsalinas})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    # def testCreateRatingUserNotPartOfProject(self):

    #     response = self.client.post(self.url, self.new_rating_data,
    #                                 format='json',
    #                                 **{'HTTP_AUTHORIZATION': self.header_rcuevas})
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

#     def testPatchRating(self):

#         response = self.client.post(self.url, self.new_rating_data,
#                                     format='json',
#                                     **{'HTTP_AUTHORIZATION': self.header_fjsalinas})
#         response = self.client.patch(self.get_id.format(self.rating))

#     def testGetClientRating(self):
#         pass

#     def testGetCollaboratorRating(self):
#         pass

#     def testDeleteRating(self):
#         pass

class RequestTestCase(APITestCase):

    def setUp(self):
        self.url = '/requests/'
        self.get_id = '/requests/{}/'
        self.get_emitter = '/requests/?emitter={}'
        self.get_project = '/requests/?project={}'
        self.get_reciever = '/requests/?reciever={}'

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

        self.user_rcuevas = User.objects.create(first_name="Robin", last_name="Cuevas",
                                                   username="rcuevas", email="rcuevas@tenecesito.cl", password="123456")
        self.user_rcuevas.set_password("123456")
        self.user_rcuevas.save()
        self.token_rcuevas = Token.objects.create(user=self.user_rcuevas)
        self.header_rcuevas = "Token {}".format(self.token_rcuevas)
        self.id_rcuevas = self.user_rcuevas.id

        self.project = Project.objects.create(
            owner=self.user_fjsalinas,
            title='Titulo Proyecto de Prueba',
            description="Descripcion del Proyecto de prueba",
            skills_required=list(['Python', 'React']),
            categories=list(['Postgresql']),
            work_modality="mixed",
            min_price_range=100000,
            max_price_range=120000,
            status="completed",
            collaborator_id=self.id_rcuevas
        )
        self.project2 = Project.objects.create(
            owner=self.user_fjherrera,
            title='Titulo Proyecto de Prueba2',
            description="Descripcion del Proyecto de prueba",
            skills_required=list(['Python', 'React']),
            categories=list(['Postgresql']),
            work_modality="mixed",
            min_price_range=100000,
            max_price_range=120000,
            status="published"
            )
        self.request = Request.objects.create(
            emitter=self.user_rcuevas,
            project=self.project2,
            why_you="Soy genial",
            requirements="Ser genial",
            price=1000
            )
        self.new_request_data = {
            "emitter": self.id_fjherrera,
            "project": self.project2.id,
            "why_you":"test",
            "requirements":"tomasin",
            "price":10000
        }
        self.new_request_data2 = {
            "emitter": self.id_fjsalinas,
            "project": self.project2.id,
            "why_you":"test",
            "requirements":"tomasin",
            "price":10000
        }
        self.new_request_data3 = {
            "emitter": self.id_rcuevas,
            "project": self.project.id,
            "why_you":"test",
            "requirements":"tomasin",
            "price":10000
        }
        self.new_request_data4 = {
            "emitter": self.id_rcuevas,
            "project": self.project2.id,
            "why_you":"test",
            "requirements":"tomasin",
            "price":10000
        }
        self.patch_data = {
            "why_you":"testingss",
            "requirements":"tomasin__222",
            "price":15000,
            "modified_project":True,
            "invited": True
        }
    def testCreateRequest(self):
        
        response = self.client.post(self.url, self.new_request_data2,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': self.header_rcuevas})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def testCreateRequestProjectNotPublished(self):

        response = self.client.post(self.url, self.new_request_data3,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': self.header_fjsalinas})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def testCreateRequestToOwnProject(self):

        response = self.client.post(self.url, self.new_request_data,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': self.header_fjsalinas})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def testCreateRequestAlreadyRequested(self):

        response = self.client.post(self.url, self.new_request_data4,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': self.header_rcuevas})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def testPatchRequest(self):

        response = self.client.patch(self.get_id.format(self.request.id), self.patch_data,
                                    format='json',
                                    **{'HTTP_AUTHORIZATION': self.header_rcuevas})
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['why_you'],
                         self.patch_data['why_you'])
        # self.assertEqual(response.data['modified_project'],
        #                  self.patch_data['modified_project'])
        self.assertEqual(response.data['price'],
                         self.patch_data['price'])
        

    def testGetEmitterRequest(self):
        pass
    def testGetProjectRequest(self):
        pass
    def testDeleteRequest(self):
        pass

    