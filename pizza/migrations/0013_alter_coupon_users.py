# Generated by Django 3.2.3 on 2021-05-15 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0012_coupon_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='users',
            field=models.ManyToManyField(blank=True, null=True, related_name='related_coupon', to='pizza.UserData'),
        ),
    ]