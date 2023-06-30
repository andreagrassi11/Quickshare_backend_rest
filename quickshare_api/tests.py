from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .views import *
from rest_framework.test import APIClient,APIRequestFactory

class NoteViewTests(TestCase):

    def setUp(self):
            self.client = APIClient()
            self.user = User.objects.create_user(username='testuser', password='testpass')
            factory = APIRequestFactory()
            user = User.objects.get(username='olivia')
            view = AccountDetail.as_view()

    def test_get(self):
        user_id = 2
        url = reverse('note', args=[int(user_id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
        
    def test_my_view(self):
        url = '/my-view/'  # Replace with your actual URL
        
        # Authenticate the client with the user
        self.client.force_authenticate(user=self.user)
        
        # Make a GET request to the URL
        response = self.client.get(url)
        
        # Assert the HTTP status code
        self.assertEqual(response.status_code, 200)
            

# class MySerializerTests(APITestCase):
#     def test_my_serializer(self):
#         data = {'name': 'John'}
#         serializer = MySerializer(data=data)
#         self.assertTrue(serializer.is_valid())
#         self.assertEqual(serializer.validated_data['name'], 'John')