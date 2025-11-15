from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class UserAuthTests(APITestCase):

    def test_user_registration(self):
        """
        Make sure we can create a new user..
        """
        register_url = reverse('register')
        user_data = {'username': 'testuser', 'password': 'a-secure-password'}
        response = self.client.post(register_url, user_data, format='json')
        
        # check that everything went well if the user was created oks
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_login(self):
        """
        test that an existing user can log in and get their token 
        """
        # First, create a user for the test
        User.objects.create_user(username='testuser', password='a-secure-password')

        # Now, try to loguin
        login_url = reverse('login')
        credentials = {'username': 'testuser', 'password': 'a-secure-password'}
        response = self.client.post(login_url, credentials, format='json')

        # see if the response is what we expect
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

