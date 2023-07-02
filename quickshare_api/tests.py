from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,force_authenticate
from .views import *
from rest_framework_simplejwt import views as jwt_views
from django.utils import timezone
from rest_framework.test import APIClient,APIRequestFactory

# User tests
class UserViewsTests(APITestCase):

    def setUp(self):
        self.username = 'usuario'
        self.password = 'contrasegna'

        self.data = {
            'username': self.username,
            'password': self.password
        }

    def test_user(self):

        # Create new user
        url = reverse('token_obtain_pair')
        user = User.objects.create_user(first_name= 'prova', 
                                        last_name='utente', 
                                        username='usuario', 
                                        email='usuario@mail.com', 
                                        password='Contrasegna123!')
        user_id = user.id

        # Take JWT for new user
        response = self.client.post(url, self.data, format='json')
        response_data = response.json() 
        access_token = response_data['access']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        return [access_token, user_id]

# Note tests
class NoteViewsTests(APITestCase):

    def setUp(self):
        self.username = 'usuario'
        self.password = 'contrasegna'

        self.data = {
            'username': self.username,
            'password': self.password
        }

        # Take data from user test
        responseUser = UserViewsTests.test_user(self)
        self.access_token = responseUser[0]
        self.user_id = responseUser[1]


    # Post view Note
    def test_post_note(self):
        
        urls = reverse('note', args=[int(self.user_id)])
        headers = {'HTTP_AUTHORIZATION': 'Bearer ' + self.access_token}
        response = self.client.post(urls, {'title': 'sgjr', 'body': 'jfsgj','create_date': timezone.now()}, **headers)
        jsonData = response.json()
        self.note_id = jsonData['note_id']
        self.assertEqual(response.status_code, 201)

    # Get view Note
    def test_get_note(self):
                
        urls = reverse('note', args=[int(self.user_id)])
        headers = {'HTTP_AUTHORIZATION': 'Bearer ' + self.access_token}
        response = self.client.get(urls, **headers)
        self.assertEqual(response.status_code, 200)
        
# Chat tests
class ChatViewsTests(APITestCase):

    def setUp(self):
        self.username = 'usuario'
        self.password = 'contrasegna'

        self.data = {
            'username': self.username,
            'password': self.password
        }

        # Take data from user test
        responseUser = UserViewsTests.test_user(self)
        self.access_token = responseUser[0]
        self.user_id = responseUser[1]

    # Post view Chat
    def test_post_chat(self):
        
        urls = reverse('chat', args=[int(self.user_id)])
        headers = {'HTTP_AUTHORIZATION': 'Bearer ' + self.access_token}
        response = self.client.post(urls, {'message': 'Messaggio prova', 'data': timezone.now(), 'fk_user_creator':self.user_id}, **headers)
        jsonData = response.json()
        self.note_id = jsonData['message_id']
        self.assertEqual(response.status_code, 201)

    # Get view Chat
    def test_get_chat(self):
                
        urls = reverse('chat', args=[int(self.user_id)])
        headers = {'HTTP_AUTHORIZATION': 'Bearer ' + self.access_token}
        response = self.client.get(urls, **headers)
        self.assertEqual(response.status_code, 200)
        