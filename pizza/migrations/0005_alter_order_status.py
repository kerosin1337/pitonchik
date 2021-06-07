# Generated by Django 3.2.3 on 2021-06-07 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pizza', '0004_alter_cartproduct_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('new', 'Новый заказ'), ('in_progress', 'Заказ в обработке'), ('is_ready', 'Заказ готов'), ('completed', 'Заказ выполнен'), ('canceled', 'Отменен')], default='new', max_length=100, verbose_name='Статус заказ'),
        ),
    ]