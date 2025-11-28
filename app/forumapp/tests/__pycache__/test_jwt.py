from django.urls import reverse
from rest_framework.test import APITestCase
from forumapp import models


class JWTAuthTests(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = models.User.objects.create_user(
            email="test@example.com",
            password="pass123",
            name="JWT Tester"
        )

    def test_obtain_jwt_token(self):
        """User should receive access + refresh tokens"""
        url = reverse('token_obtain_pair')
        data = {
            "email": "test@example.com",
            "password": "pass123"
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
