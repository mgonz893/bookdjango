# Generated by Django 3.0.2 on 2020-02-03 01:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0012_auto_20200202_1801'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BookInstance',
        ),
    ]