from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (HabitsCreateAPIView, HabitsDeleteAPIView,
                          HabitsDetailAPIView, HabitsListAPIView,
                          HabitsUpdateAPIView)

app_name = HabitsConfig.name


urlpatterns = [
    path("habit/create/", HabitsCreateAPIView.as_view(), name="habit_create"),
    path("habits/", HabitsListAPIView.as_view(), name="habits_list"),
    path("habit/<int:pk>/", HabitsDetailAPIView.as_view(), name="habit"),
    path("habit/update/<int:pk>/", HabitsUpdateAPIView.as_view(), name="habit_update"),
    path("habit/delete/<int:pk>/", HabitsDeleteAPIView.as_view(), name="habit_delete"),
]
