# Generated by Django 3.0.2 on 2020-03-22 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0039_auto_20200321_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderbook',
            name='tot_quantity',
            field=models.FloatField(default=1.0),
        ),
    ]