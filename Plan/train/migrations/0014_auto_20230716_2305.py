# Generated by Django 2.2.16 on 2023-07-16 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0013_auto_20230411_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='donemaidate',
            name='place',
            field=models.CharField(choices=[('ЕКБ', 'Екатеринбург'), ('ЧЛБ', 'Челябинск'), ('Пермь', 'Пермь'), ('МСК', 'Москва'), ('СПБ', 'Санкт-Петербург'), ('Сочи', 'Сочи'), ('Крюково', 'Крюково'), ('КЛГ', 'Калининград')], default='ЕКБ', max_length=30, verbose_name='Место проведения'),
        ),
    ]