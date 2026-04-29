from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthTests(APITestCase):

    def setUp(self):
        self.register_url = "/api/auth/register/"
        self.login_url = "/api/auth/login/"

    def test_register_success(self):
        data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "strongpass123",
            "password2": "strongpass123",
        }

        response = self.client.post(self.register_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token", response.data)
        self.assertEqual(User.objects.count(), 1)

    def test_register_password_mismatch(self):
        data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "123456",
            "password2": "wrong",
        }

        response = self.client.post(self.register_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_login_success(self):
        User.objects.create_user(
            username="testuser",
            email="test@test.com",
            password="strongpass123"
        )

        data = {
            "username": "testuser",
            "password": "strongpass123",
        }

        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_wrong_password(self):
        User.objects.create_user(
            username="testuser",
            password="correctpass"
        )

        data = {
            "username": "testuser",
            "password": "wrongpass",
        }

        response = self.client.post(self.login_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_access_protected_without_token(self):
        response = self.client.get("/api/weather/?city=Kyiv")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
