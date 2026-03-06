from rest_framework import serializers

from habits.models import Habit

class HabitListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = ["id", "user", "action", "is_public"]


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        reward = data.get("reward")
        related_habit = data.get("related_habit")
        is_pleasant = data.get("is_pleasant")
        execution_time = data.get("execution_time")
        periodicity = data.get("periodicity")

        # 1. Нельзя одновременно reward и related_habit
        if self.instance:
            reward = reward if reward is not None else self.instance.reward
            related_habit = related_habit if related_habit is not None else self.instance.related_habit

        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )

        # 2. Время выполнения <= 120 секунд
        if execution_time and execution_time > 120:
            raise serializers.ValidationError(
                "Время выполнения не может превышать 120 секунд."
            )

        # 3. Связанная привычка должна быть приятной
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной."
            )

        # 4. У приятной привычки не может быть reward или related_habit
        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        # 5. Нельзя реже чем 1 раз в 7 дней
        if periodicity and periodicity > 7:
            raise serializers.ValidationError(
                "Нельзя выполнять привычку реже чем 1 раз в 7 дней."
            )

        return data
