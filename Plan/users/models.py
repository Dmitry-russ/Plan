from django.db import models
from django.contrib.auth import get_user_model
from train.models import CreatedModel

User = get_user_model()


class UserData(CreatedModel):
    """Расширение модели User"""
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               null=False,
                               related_name='userdata', )

    telegram = models.TextField(
        verbose_name="Телеграм (ник)", unique=True,
    )

    def __str__(self) -> str:
        return self.telegram
