from rest_framework.exceptions import ValidationError


class HabitValidator:
    """Класс валидатор вынесен для не заграмождения Сериализатора"""

    def __call__(self, data):

        execution_time = data.get("execution_time")
        periodicity = data.get("periodicity")
        related_habit = data.get("related_habit")

        if execution_time and execution_time > 120:
            raise ValidationError("Время выполнения не может превышать 120 секунд.")

        if periodicity and periodicity > 7:
            raise ValidationError("Нельзя выполнять привычку реже чем 1 раз в 7 дней.")

        if related_habit and not related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        return data
