# Generated by Django 3.0.2 on 2020-02-23 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0026_orderbook_order_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderbook',
            name='order_price',
        ),
    ]
