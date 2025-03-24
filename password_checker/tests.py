from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Password
import hashlib

class PasswordCheckTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        compromised_password = "azerty"
        compromised_hash = hashlib.sha1(compromised_password.encode('utf-8')).hexdigest()
        Password.objects.create(hash=compromised_hash)

    def test_password_compromised(self):
        response = self.client.post('/api/check-password/', {'password': 'azerty'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.json()['compromised'])
        self.assertEqual(len(response.json()['recommendations']), 4)

    def test_password_uncompromised(self):
        response = self.client.post('/api/check-password/', {'password': '?Azerty!!9582*'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()['compromised'])
        self.assertEqual(len(response.json()['recommendations']), 0)

    def test_too_short_password(self):
        response = self.client.post('/api/check-password/', {'password': 'azert'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()['compromised'])
        self.assertIn("Le mot de passe doit comporter au moins 12 caractères.", response.json()['recommendations'])

    def test_password_without_number(self):
        response = self.client.post('/api/check-password/', {'password': 'azertynonumber!'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()['compromised'])
        self.assertIn("Le mot de passe doit contenir des chiffres.", response.json()['recommendations'])

    def test_password_without_special_char(self):
        response = self.client.post('/api/check-password/', {'password': 'azerty1nospecialchar'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.json()['compromised'])
        self.assertIn("Le mot de passe doit contenir des caractères spéciaux.", response.json()['recommendations'])

    def test_blank_field(self):
        response = self.client.post('/api/check-password/', {'password': ''}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
