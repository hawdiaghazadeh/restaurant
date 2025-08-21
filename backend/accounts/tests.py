from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AccountsTests(APITestCase):
    def setUp(self):
        self.register_url = "/api/accounts/register/"
        self.login_url = "/api/accounts/login/"
        self.logout_url = "/api/accounts/logout/"
        self.change_password_url = "/api/accounts/change_password/"

        self.user_data = {
            "email":"google1@gmail.com",
            "password":"TestPassword",
            "password2":"TestPassword",
        }

    def test_register(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, self.user_data["email"])


    def test_login(self):
        User.objects.create_user(email=self.user_data["email"], password=self.user_data["password"])

        login_data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }

        response = self.client.post(self.login_url, login_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.cookies)
        self.assertIn("refresh_token", response.cookies)

    def test_logout(self):
        user = User.objects.create_user(email=self.user_data['email'], password=self.user_data['password'])

        self.client.force_authenticate(user=user)
        response = self.client.post(self.logout_url, self.user_data, format="json")

    def test_change_password(self):
        user = User.objects.create_user(email=self.user_data['email'], password=self.user_data['password'])
        self.client.force_authenticate(user=user)

        new_password_data = {
            "old_password": self.user_data['password'],
            "password": "new123456789",
            "password2": "new123456789"
        }

        response = self.client.post(self.change_password_url, new_password_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
