# Generated by Django 2.2.16 on 2023-03-01 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('train', '0009_cases_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cases',
            name='file',
            field=models.FileField(null=True, upload_to='cases/'),
        ),
    ]