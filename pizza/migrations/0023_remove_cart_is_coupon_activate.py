# Generated by Django 3.2.3 on 2021-05-17 04:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0022_remove_coupon_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='is_coupon_activate',
        ),
    ]