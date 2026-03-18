from django.db.models import Q
from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
)

from habits.models import Habit
from habits.paginators import MyPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitListSerializer, HabitSerializer


class HabitsCreateAPIView(CreateAPIView):
    """Создание привычки с автоматическим присвоением поля авторизованного пользователя"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitsListAPIView(ListAPIView):
    """Это у нас вывод списка через ИИ =)
    Выдаёт список своих + публичных привычек"""

    serializer_class = HabitListSerializer
    pagination_class = MyPaginator

    def get_queryset(self):
        user = self.request.user

        return Habit.objects.filter(Q(user=user) | Q(is_public=True))


class HabitsDetailAPIView(RetrieveAPIView):
    """Подробные детали одной привычки"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class HabitsUpdateAPIView(UpdateAPIView):
    """Редактировать привычку"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class HabitsDeleteAPIView(DestroyAPIView):
    """Удалить привычку"""

    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]
