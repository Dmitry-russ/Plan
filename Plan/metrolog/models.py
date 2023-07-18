from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models
from train.models import CreatedModel, ALL_PLACE_CHOICES

User = get_user_model()
TEXT_FIELD_MAX_LENGTH = 100
METROLOG_TYPE = [
    ("Калибровка", 'Калибровка'),
    ("Поверка", 'Поверка'),
]


class Measurement(CreatedModel):
    """Модель инструмента (системы измерения)."""

    PLACE_CHOICES = ALL_PLACE_CHOICES
    METROLOG_CONTROL = METROLOG_TYPE
    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               null=True,
                               related_name='measurement', )
    type = models.CharField(
        verbose_name="Тип СИ", max_length=TEXT_FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )
    dunumber = models.CharField(
        verbose_name="Номер DU", max_length=TEXT_FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )
    description = models.TextField(
        verbose_name="Описание", max_length=TEXT_FIELD_MAX_LENGTH,
    )
    location = models.CharField(
        max_length=30,
        choices=PLACE_CHOICES,
        default="ЕКБ",
        verbose_name="Локация"
    )
    model = models.CharField(
        verbose_name="Модель СИ", max_length=TEXT_FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )
    maker = models.CharField(
        verbose_name="Производитель", max_length=TEXT_FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )
    number = models.CharField(
        verbose_name="Номер в госреестре", max_length=TEXT_FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )
    control_type = models.CharField(
        max_length=30,
        choices=METROLOG_CONTROL,
        default="Поверка",
        verbose_name="Тип метрологического контроля"
    )
    periodicity = models.IntegerField(
        verbose_name="Периодичность проверки, мес.",
    )
    organization = models.CharField(
        verbose_name="Организация для направления в поверку",
        max_length=TEXT_FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )
    organization_fact = models.CharField(
        verbose_name="Фактическая организация, проводившая поверку",
        max_length=TEXT_FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )
    seral_number = models.CharField(
        verbose_name="Серийный номер", max_length=TEXT_FIELD_MAX_LENGTH,
    )
    date_control = models.DateField(
        verbose_name="Дата проверки",
    )
    date_end = models.DateField(
        verbose_name="Дата окончания поверки",
    )
    place = models.CharField(
        verbose_name="Фактическое местоположение",
        max_length=TEXT_FIELD_MAX_LENGTH,
    )
    in_act = models.BooleanField(
        verbose_name="Наличие в акте РЖД",
        default=False,
    )
    note = models.TextField(
        verbose_name="Примечание",
        max_length=TEXT_FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )

    def get_days(self):
        date_end = datetime.strptime(
            str(self.date_end), '%Y-%m-%d')
        current_date = datetime.strptime(
            str(datetime.now().date()), '%Y-%m-%d')
        diff = date_end - current_date
        days = diff.days
        return days

    def __str__(self) -> str:
        return self.description


class Certificate(CreatedModel):
    """Модель хранения файлов сертификатов."""

    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               related_name='certificate',
                               null=True, )
    metrolog = models.ForeignKey(Measurement,
                                 on_delete=models.CASCADE,
                                 related_name='certificate')
    name = models.CharField(
        max_length=TEXT_FIELD_MAX_LENGTH,
        blank=True,
        verbose_name="Название сертификата", )
    file = models.FileField(blank=True,
                            null=True,
                            upload_to='metrolog/',
                            verbose_name="Новый сертификат", )
    default = models.BooleanField(default=True)


class Manual(CreatedModel):
    """Модель хранения РЭ."""

    author = models.ForeignKey(User,
                               on_delete=models.SET_NULL,
                               related_name='manual',
                               null=True, )
    metrolog = models.ForeignKey(Measurement,
                                 on_delete=models.CASCADE,
                                 related_name='manual')
    name = models.CharField(max_length=TEXT_FIELD_MAX_LENGTH, blank=True, )
    file = models.FileField(blank=True,
                            null=True,
                            upload_to='metrolog/',
                            verbose_name="Руководство", )
    default = models.BooleanField(default=True)
