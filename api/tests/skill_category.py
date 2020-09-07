from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from api.models import Skill, User, Category
import json
from rest_framework import status


# class SkillTestCase(APITestCase):

#     def setUp(self):
#         self.user_fjsalinas = User.objects.create(first_name="Fernando", last_name="Salinas",
#                                                   username="fjsalinas", email="fjsalinas@tenecesito.cl")
#         self.user_fjsalinas.set_password("123456")
#         self.user_fjsalinas.save()
#         self.token_fjsalinas = Token.objects.create(user=self.user_fjsalinas)
#         self.header_fjsalinas = 'Token {}'.format(self.token_fjsalinas)

#         self.category = Category.objects.create(name="Websites, IT & Software")

#     def testCreateSkill(self):

#         response = self.client.post(
#             f'/skills/',
#             {'name': 'Python',
#              'category': self.category.id},
#             format='json',
#             **{'HTTP_AUTHORIZATION': self.header_fjsalinas})
#         print(response.content)
