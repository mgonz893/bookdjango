# Generated by Django 3.0.2 on 2020-03-21 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0036_auto_20200321_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='savebook',
            name='tot_quantity',
            field=models.IntegerField(default=1),
        ),
    ]
