# Generated by Django 3.2.3 on 2021-05-15 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0009_auto_20210515_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='sale',
            field=models.DecimalField(decimal_places=2, max_digits=3, verbose_name='Скидка'),
        ),
    ]
