# Generated by Django 3.2.4 on 2021-06-14 14:17

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True, unique=True, validators=[django.core.validators.RegexValidator('[0-9]{1}-[0-9]{3}-[0-9]{3}-[0-9]{2}-[0-9]{2}')], verbose_name='Номер телефона'),
        ),
    ]