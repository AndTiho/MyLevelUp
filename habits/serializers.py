from rest_framework import serializers

from habits.models import Habit
from habits.validators import HabitValidator


class HabitListSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода списка привычек"""

    class Meta:
        model = Habit
        fields = ["id", "user", "action", "is_public"]


class HabitSerializer(serializers.ModelSerializer):
    """Сериализатор для CRUD привычек с валидаторами, которые требуют обращения к self"""

    class Meta:
        model = Habit
        fields = "__all__"
        validators = [HabitValidator()]

    def validate(self, data):

        reward = data.get("reward")
        related_habit = data.get("related_habit")
        is_pleasant = data.get("is_pleasant")

        if self.instance:
            reward = reward if reward is not None else self.instance.reward
            related_habit = (
                related_habit
                if related_habit is not None
                else self.instance.related_habit
            )
            is_pleasant = (
                is_pleasant if is_pleasant is not None else self.instance.is_pleasant
            )

        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )

        if self.instance and related_habit and related_habit.id == self.instance.id:
            raise serializers.ValidationError(
                "Нельзя привязывать привычку к самой себе."
            )

        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        return data
