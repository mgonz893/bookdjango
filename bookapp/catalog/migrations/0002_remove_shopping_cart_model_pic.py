# Generated by Django 3.0.2 on 2020-02-15 01:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopping_cart',
            name='model_pic',
        ),
    ]
