# Generated by Django 3.2.3 on 2021-05-24 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdata',
            name='session',
        ),
        migrations.AddField(
            model_name='cart',
            name='session',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]