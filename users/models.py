from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Стандартная модель пользователя, без каких либо требований."""

    tg_chat_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Телеграм chat_id"
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ["username"]

