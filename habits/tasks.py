import requests
from celery import shared_task
from django.utils.timezone import now

from config import settings
from habits.models import Habit


@shared_task
def send_telegram_message(chat_id, message):
    """Отправка сообщения в телеграм"""

    params = {
        "text": message,
        "chat_id": chat_id,
    }
    requests.get(
        f"{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage", params=params
    )


@shared_task
def check_habits():
    """Проверяет все привычки на предмет переодичности отправки и выполняет в назначенное время отложеную задачу."""

    current_time = now().time()
    today = now().date()
    habits = Habit.objects.all()

    for habit in habits:

        last_run = (habit.last_run or habit.created_at).date()
        days_passed = (today - last_run).days

        if (
            habit.time.hour == current_time.hour
            and habit.time.minute == current_time.minute
            and days_passed >= habit.periodicity
        ):
            send_telegram_message.delay(
                habit.user.tg_chat_id, f"Пора выполнить привычку: {habit.action}"
            )

            habit.last_run = today
            habit.save()
