# Generated by Django 3.2.3 on 2021-06-01 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0005_promotions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='promotions',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pizza.products'),
        ),
    ]