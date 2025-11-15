from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Prompt
from rest_framework_simplejwt.tokens import RefreshToken


class PromptTests(APITestCase):

    def setUp(self):
        # prepare everything for the tests
        self.user = User.objects.create_user(username='testuser', password='a-secure-password')
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token.access_token}')

    def test_create_a_prompt(self):
        """
        Let's test if a new prompt can be created.
        """
        url = reverse('prompt-create')
        prompt_data = {'text': 'This is a test prompt'}
        response = self.client.post(url, prompt_data, format='json')

        # check if it was created correctly
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Prompt.objects.count(), 1)
        self.assertEqual(Prompt.objects.get().prompt, 'This is a test prompt')

    def test_get_similar_prompts(self):
        """
        Let's see if the similar prompts thing works.
        """
        # Create a prompt to have something to compare against
        Prompt.objects.create(user=self.user, prompt='an initial prompt', response='resp', embedding=[0.1, 0.2, 0.3])
        
        url = reverse('similar_prompt')
        response = self.client.get(url, {'prompt': 'a similar prompt'})

        # check the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('similars', response.data)

