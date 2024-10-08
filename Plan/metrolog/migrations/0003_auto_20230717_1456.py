# Generated by Django 2.2.16 on 2023-07-17 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('metrolog', '0002_auto_20230717_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='organization',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Организация для направления в поверку'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='organization_fact',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Фактическая организация, проводившая поверку'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='description',
            field=models.TextField(max_length=100, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='dunumber',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер DU'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='maker',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Производитель'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='model',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Модель СИ'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='note',
            field=models.TextField(blank=True, max_length=100, null=True, verbose_name='Примечание'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Номер в госреестре'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='type',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Тип СИ'),
        ),
    ]
