# Generated by Django 3.0.2 on 2020-02-15 01:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_remove_shopping_cart_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopping_cart',
            name='name',
            field=models.CharField(default='Shopping Cart', max_length=100),
        ),
    ]