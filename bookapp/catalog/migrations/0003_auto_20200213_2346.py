# Generated by Django 3.0.2 on 2020-02-14 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20200213_2330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderbook',
            name='book',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.Book'),
        ),
    ]
