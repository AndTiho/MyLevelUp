from django.db.models import Q
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)

from habits.models import Habit
from habits.paginators import MyPaginator
from habits.serializers import HabitSerializer
from users.permissions import IsOwner


class HabitsCreateAPIView(CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class HabitsListAPIView(ListAPIView):
    """ Это у нас вывод списка через ИИ =)
    Выдаёт список своих + публичных привычек"""

    serializer_class = HabitSerializer
    pagination_class = MyPaginator

    def get_queryset(self):
        user = self.request.user

        return Habit.objects.filter(
            Q(user=user) | Q(is_public=True)
        )


class HabitsDetailAPIView(RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class HabitsUpdateAPIView(UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]


class HabitsDeleteAPIView(DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsOwner]
