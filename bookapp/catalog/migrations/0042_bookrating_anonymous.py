# Generated by Django 3.0.2 on 2020-03-27 22:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0041_remove_orderbook_tot_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookrating',
            name='anonymous',
            field=models.BooleanField(default=False, verbose_name='Post as anonymous'),
        ),
    ]