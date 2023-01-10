from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models

TEXT_FIELD_MAX_LENGTH = 5
VALIDATE_PARAM=[MinLengthValidator(
            3, message='Должно быть больше двух символов.'
        )]



class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""

    created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['created']),
        ]

class Serial(CreatedModel):
    """Модель серии поезда."""
    serial = models.TextField(
        verbose_name="Серия", max_length=TEXT_FIELD_MAX_LENGTH,
        validators=VALIDATE_PARAM, unique=True,
        )
    slug = models.SlugField(verbose_name="Слаг",
                            max_length=TEXT_FIELD_MAX_LENGTH,
                            null=False,
                            unique=True,
        validators=VALIDATE_PARAM
                             )
    

class Train(CreatedModel):
    """Модель поезда."""
    serial = models.ForeignKey(Serial,
                               verbose_name="Серия",
                               on_delete=models.CASCADE,
                               related_name='train')


    number = models.CharField(
        verbose_name="Номер",
        max_length=TEXT_FIELD_MAX_LENGTH,
        null=False,
        validators=VALIDATE_PARAM
        )
    
    renter = models.CharField(
        verbose_name="Арендатор",
        max_length=TEXT_FIELD_MAX_LENGTH,
        null=False
    )

    mileage = models.IntegerField(
        verbose_name="Пробег")
    mileage_date = models.DateField(
        verbose_name="Дата считывания пробега")
    day_mileage = models.IntegerField(
        verbose_name="Среднесуточный пробег")

    image = models.ImageField(
        'Фото',
        upload_to='Plan/',
        blank=True
    )
    class Meta:
        ordering = ["serial", "number"]
        constraints = [
            models.UniqueConstraint(fields=["serial", "number"],
                                    name="serial_number")
        ]
class DoneMaiDate(CreatedModel):
    """Модель хранения данных о проведенных ТО."""
    MAINTENANCE_CHOICES = [
        ("Vi", 'Vi'),
        ("I1", 'I1'),
        ("I2", 'I2'),
        ("I3", 'I3'),
        ("I4", 'I4'),
        ("I4+I5", 'I4+I5'),
        ("I5", 'I5'),
        ("I6", 'I6'),
        ("30", '30 суток'),
    ]
    PLACE_CHOICES = [
        ("ЕКБ", 'Екатеринбург'),
        ("ЧЛБ", 'Челябинск'),
        ("Пермь", 'Пермь'),
        ("МСК", 'Москва'),
        ("СПБ", 'Санкт-Петербург'),
        ("Сочи", 'Сочи'),
        ("Крюково", 'Крюково'),
    ]
    train = models.ForeignKey(Train,
                               verbose_name="Поезд",
                               on_delete=models.CASCADE,
                               related_name='maintenance')

    maintenance = models.CharField(
        max_length=2,
        choices=MAINTENANCE_CHOICES,
        default="Vi",
        verbose_name="Вид ТО"
    )

    maintenance_date = models.DateField(
        verbose_name="Дата")
    place = models.CharField(
        max_length=2,
        choices=MAINTENANCE_CHOICES,
        default="ЕКБ",
        verbose_name="Место проведения"
    )

    mileage = models.IntegerField(
        verbose_name="Пробег")
    class Meta:
        ordering = ["-maintenance_date"]
        constraints = [
            models.UniqueConstraint(fields=["train", "maintenance_date"],
                                    name="train_maintenance_date")
        ]


class PlanMaiDate(CreatedModel):
    """Модель хранения данных о запланированных ТО."""
    MAINTENANCE_CHOICES = [
        ("Vi", 'Vi'),
        ("I1", 'I1'),
        ("I2", 'I2'),
        ("I3", 'I3'),
        ("I4", 'I4'),
        ("I4+I5", 'I4+I5'),
        ("I5", 'I5'),
        ("I6", 'I6'),
        ("30", '30 суток'),
    ]
    PLACE_CHOICES = [
        ("ЕКБ", 'Екатеринбург'),
        ("ЧЛБ", 'Челябинск'),
        ("Пермь", 'Пермь'),
        ("МСК", 'Москва'),
        ("СПБ", 'Санкт-Петербург'),
        ("Сочи", 'Сочи'),
        ("Крюково", 'Крюково'),
    ]
    train = models.ForeignKey(Train,
                               verbose_name="Поезд",
                               on_delete=models.CASCADE,
                               related_name='plan')
    maintenance = models.CharField(
        max_length=2,
        choices=MAINTENANCE_CHOICES,
        default="Vi",
        verbose_name="Вид ТО",
    )

    place = models.CharField(
        max_length=2,
        choices=MAINTENANCE_CHOICES,
        default="ЕКБ",
        verbose_name="Место проведения",
    )
    mileage = models.IntegerField(
        verbose_name="Пробег",
        blank=True,
        )
