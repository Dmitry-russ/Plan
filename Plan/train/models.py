from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

TEXT_FIELD_MAX_LENGTH = 5
MAX_LEN_CASES_SMALL_CALL = 150
MAX_LEN_CASES_BIG_CALL = 500
VALIDATE_PARAM=[MinLengthValidator(
            3, message='Должно быть больше двух символов.'
        )]
ALL_MAINTENANCE_CHOICES = [
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
ALL_PLACE_CHOICES = [
        ("ЕКБ", 'Екатеринбург'),
        ("ЧЛБ", 'Челябинск'),
        ("Пермь", 'Пермь'),
        ("МСК", 'Москва'),
        ("СПБ", 'Санкт-Петербург'),
        ("Сочи", 'Сочи'),
        ("Крюково", 'Крюково'),
    ]


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
    author = models.ForeignKey(User,
                               on_delete=models.SET_DEFAULT,
                               related_name='serial',
                               default = 'нет',)
    serial = models.TextField(
        verbose_name="Серия", max_length=TEXT_FIELD_MAX_LENGTH,
        validators=VALIDATE_PARAM, unique=True,
        )
    slug = models.SlugField(verbose_name="Слаг",
                            max_length=TEXT_FIELD_MAX_LENGTH,
                            unique=True,
                            validators=VALIDATE_PARAM
                             )
    

class Train(CreatedModel):
    """Модель поезда."""
    author = models.ForeignKey(User,
                               on_delete=models.SET_DEFAULT,
                               related_name='train',
                               default = 'нет',)
    serial = models.ForeignKey(Serial,
                               verbose_name="Серия",
                               on_delete=models.CASCADE,
                               related_name='train')


    number = models.CharField(
        verbose_name="Номер",
        max_length=TEXT_FIELD_MAX_LENGTH,
        validators=VALIDATE_PARAM,
        )
    
    renter = models.CharField(
        verbose_name="Арендатор",
        max_length=TEXT_FIELD_MAX_LENGTH,
        blank=True,
        null=True,
    )

    mileage = models.IntegerField(
        verbose_name="Пробег на дату",
        blank=True,
        null=True,
        )
    mileage_date = models.DateField(
        verbose_name="Дата считывания пробега",
        blank=True,
        null=True,
        )
    day_mileage = models.IntegerField(
        verbose_name="Среднесуточный пробег",
        blank=True,
        null=True,
        )

    image = models.ImageField(
        'Фото',
        upload_to='Plan/',
        blank=True,
        null=True,
    )
    class Meta:
        ordering = ["serial", "number"]
        constraints = [
            models.UniqueConstraint(fields=["serial", "number"],
                                    name="serial_number")
        ]
class DoneMaiDate(CreatedModel):
    """Модель хранения данных о проведенных ТО."""

    MAINTENANCE_CHOICES = ALL_MAINTENANCE_CHOICES
    PLACE_CHOICES = ALL_PLACE_CHOICES
    author = models.ForeignKey(User,
                               on_delete=models.SET_DEFAULT,
                               related_name='maintenance',
                               default = 'нет',)
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
    MAINTENANCE_CHOICES = ALL_MAINTENANCE_CHOICES
    PLACE_CHOICES = ALL_PLACE_CHOICES
    author = models.ForeignKey(User,
                               on_delete=models.SET_DEFAULT,
                               related_name='plan',
                               default = 'нет',)
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

    date_one = models.DateField(
        verbose_name="Дата начала ТО")
    date_two = models.DateField(
        verbose_name="Дата окончания ТО")

    place = models.CharField(
        max_length=2,
        choices=MAINTENANCE_CHOICES,
        default="ЕКБ",
        verbose_name="Место проведения",
        blank=True,
    )
    mileage = models.IntegerField(
        verbose_name="Пробег",
        blank=True,
        )


class Cases(CreatedModel):
    """Модель хранения замечаний."""
    author = models.ForeignKey(User,
                               on_delete=models.SET_DEFAULT,
                               related_name='cases',
                               default = 'нет')
    train = models.ForeignKey(Train,
                               verbose_name="Поезд",
                               on_delete=models.CASCADE,
                               related_name='cases')
    name = models.CharField(
        verbose_name="Короткое описание",
        max_length=MAX_LEN_CASES_SMALL_CALL,
        blank=False,
    )
    text = models.CharField(
        max_length = MAX_LEN_CASES_BIG_CALL,
        verbose_name="Полное описание",
        blank=True,
    )


class Image(models.Model):
    """Модель хранения изображений замечания."""
    author = models.ForeignKey(User,
                               on_delete=models.SET_DEFAULT,
                               related_name='image',
                               default = 'нет')
    cases = models.ForeignKey(Cases, 
                              on_delete=models.CASCADE,
                              related_name='image')
    name = models.CharField(max_length=MAX_LEN_CASES_SMALL_CALL, blank=True,)
    image = models.ImageField(upload_to='images/')
    default = models.BooleanField(default=False)
