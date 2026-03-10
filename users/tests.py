from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserAPITestCase(APITestCase):

    def setUp(self):
        self.user_1 = User.objects.create_user(username="test_user_1", password="123")
        self.user_2 = User.objects.create_user(username="test_user_2", password="123")

    def tearDown(self):
        """Сносим всё до начала тестов каждый раз, чтобы небыло конфликтов"""
        User.objects.all().delete()

    def test_create_user(self):
        """Тестим создание пользователя"""

        # Основная дата для создания
        data = {
            "username": "test_user_3",
            "password": "123",
        }

        response = self.client.post("/users/register/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "test_user_3")
        self.assertTrue(User.objects.filter(username="test_user_3").exists())

        user = User.objects.get(username="test_user_3")
        self.assertTrue(user.check_password("123"))

    def test_update_permissions_user(self):
        """Тест на права доступа к внесению изменений в модель юзера"""

        # Основные данные для патча
        data = {
            "first_name": "Test First Name",
            "last_name": "Test Last Name",
        }

        # Проверяем, что без у пользователя без авторизации нет на это прав
        response = self.client.patch(
            f"/users/{self.user_1.id}/update/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Проверяем, что у пользователя "НЕ ВЛАДЕЛЬЦА" тоже нет на это прав
        self.client.force_authenticate(user=self.user_2)
        response = self.client.patch(
            f"/users/{self.user_1.id}/update/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Проверяем, что пользователь владелец имеет на это права
        self.client.force_authenticate(user=self.user_1)
        response = self.client.patch(
            f"/users/{self.user_1.id}/update/", data=data, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
