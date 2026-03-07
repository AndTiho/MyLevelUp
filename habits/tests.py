from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


# Create your tests here.
class HabitsAPITestCase(APITestCase):

    def setUp(self):
        self.user_1 = User.objects.create_user(username='test_user_1', password='123')
        self.user_2 = User.objects.create_user(username='test_user_2', password='123')
        self.habit_1 = Habit.objects.create(place='Test', time='15:00', action='Test', execution_time=60,
                                            user=self.user_1)
        self.habit_2_is_public = Habit.objects.create(place='Test', time='15:00', action='Test', execution_time=60,
                                                      is_public=True,
                                                      user=self.user_2)
        self.habit_1_is_pleasant = Habit.objects.create(place='Test', time='15:00', action='Test', execution_time=60,
                                                        is_pleasant=True, user=self.user_1)
        self.habit_1_is_pleasant_1 = Habit.objects.create(place='Test', time='15:00', action='Test', execution_time=60,
                                                        is_pleasant=True, user=self.user_1)
        self.habit_1_with_reward = Habit.objects.create(place='Test', time='15:00', action='Test', execution_time=60,
                                                        reward='test',
                                                        user=self.user_1)

    def tearDown(self):
        """Сносим всё до начала тестов каждый раз, чтобы небыло конфликтов"""
        Habit.objects.all().delete()

    def test_create_habit(self):
        """Тестируем создание привычки"""

        # Основные данные для привычки
        data = {
            'place': 'Test',
            'time': '15:00',
            'action': 'Test',
            'execution_time': '60'
        }

        # Проверяем, что у не авторизованного пользователя нет на это прав
        response = self.client.post("/habits/create/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Продолжаем тестирование, авторизуя пользователя
        self.client.force_authenticate(user=self.user_1)
        response = self.client.post("/habits/create/", data=data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 6)
        self.assertEqual(response.data["place"], "Test")
        self.assertEqual(response.data["action"], "Test")
        self.assertEqual(response.data["time"], "15:00:00")
        self.assertEqual(response.data["execution_time"], 60)

        self.assertTrue(Habit.objects.filter(id=1).exists())

    def test_update_habit(self):
        """Тестируем обновление данных в привычке"""

        # Основные данные для теста
        data = {
            "place": "Test place updated",
            "action": "Test action updated",
        }

        # Проверяем, что у не авторизованного пользователя нет на это прав
        response = self.client.patch(f"/habits/update/{self.habit_1.id}/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Проверяем, что у пользователя не владельца тоже нет прав на изменение привычки
        self.client.force_authenticate(user=self.user_2)
        response = self.client.patch(f"/habits/update/{self.habit_1.id}/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Продолжаем тестирование, авторизуя пользователя
        self.client.force_authenticate(user=self.user_1)
        response = self.client.patch(f"/habits/update/{self.habit_1.id}/", data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["place"], "Test place updated")
        self.assertEqual(response.data["action"], "Test action updated")
        self.assertEqual(response.data["time"], "15:00:00")
        self.assertEqual(response.data["execution_time"], 60)

    def test_detail_habit(self):
        """Тестируем детальный вид привычки"""

        # Проверяем, что у не авторизованного пользователя нет на это прав
        response = self.client.get(f"/habits/{self.habit_1.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Проверяем, что у пользователя не владельца тоже нет прав на это права
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(f"/habits/{self.habit_1.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Продолжаем тестирование, авторизуя пользователя
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(f"/habits/{self.habit_1.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(
            response.json(),
            {
                "id": response.data['id'],
                "place": "Test",
                "time": "15:00:00",
                "action": "Test",
                "is_pleasant": False,
                "periodicity": 1,
                "reward": None,
                "execution_time": 60,
                "is_public": False,
                "created_at": response.data['created_at'],
                "last_run": None,
                "user": response.data['user'],
                "related_habit": None
            }
        )

    def test_delete_habit(self):
        """Тестируем удаление привычки"""

        # Проверяем, что у не авторизованного пользователя нет на это прав
        response = self.client.delete(f"/habits/delete/{self.habit_1.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Проверяем, что у пользователя не владельца тоже нет прав на это права
        self.client.force_authenticate(user=self.user_2)
        response = self.client.delete(f"/habits/delete/{self.habit_1.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Продолжаем тестирование, авторизуя пользователя
        self.client.force_authenticate(user=self.user_1)
        response = self.client.delete(f"/habits/delete/{self.habit_1.id}/", format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_list_habit(self):
        """Тестируем вывод списка привычек"""

        # Проверяем, что у не авторизованного пользователя нет на это прав
        response = self.client.get(f"/habits/", format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Проверяем, что пользователь не владелец видит только свои привычки
        self.client.force_authenticate(user=self.user_2)
        response = self.client.get(f"/habits/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

        # Проверяем, что пользователь видит свои привычки и привычки с признаком is_public, то есть все
        self.client.force_authenticate(user=self.user_1)
        response = self.client.get(f"/habits/", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 5)

    def test_validators_habit(self):
        """Отдельно протестируем валидацию данных на update"""

        # Завозим юзера
        self.client.force_authenticate(user=self.user_1)

        # 1. Нельзя одновременно reward и related_habit
        response = self.client.patch(f"/habits/update/{self.habit_1.id}/",
                                     data={"reward": "Test", "related_habit": self.habit_1_is_pleasant_1.id}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Нельзя одновременно указывать вознаграждение и связанную привычку."
        )

        # 2. Время выполнения <= 120 секунд
        response = self.client.patch(f"/habits/update/{self.habit_1.id}/", data={"execution_time": 121}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Время выполнения не может превышать 120 секунд."
        )

        # 3. Связанная привычка должна быть приятной
        response = self.client.patch(f"/habits/update/{self.habit_1.id}/",
                                     data={"related_habit": self.habit_2_is_public.id}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Связанная привычка должна быть приятной."
        )

        # 4. У приятной привычки не может быть reward
        response = self.client.patch(f"/habits/update/{self.habit_1_is_pleasant.id}/", data={"reward": "Test"},
                                     format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )

        # 4. У приятной привычки не может быть related_habit
        response = self.client.patch(f"/habits/update/{self.habit_1_is_pleasant.id}/",
                                     data={"related_habit": self.habit_1_is_pleasant_1.id}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )

        # 5. Нельзя реже чем 1 раз в 7 дней
        response = self.client.patch(f"/habits/update/{self.habit_1.id}/", data={"periodicity": 8}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Нельзя выполнять привычку реже чем 1 раз в 7 дней."
        )

        # 6. Нельзя привязывать саму себя
        response = self.client.patch(f"/habits/update/{self.habit_1_is_pleasant.id}/",
                                     data={"related_habit": self.habit_1_is_pleasant.id}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["non_field_errors"][0],
            "Нельзя привязывать привычку к самой себе."
        )

    def test_other_some_code(self):
        self.assertEqual(str(self.habit_1), "Я буду Test в 15:00 в Test")
        self.assertEqual(str(self.user_1), "test_user_1")
