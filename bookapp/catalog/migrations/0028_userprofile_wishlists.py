# Generated by Django 3.0.2 on 2020-03-01 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0027_remove_orderbook_order_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='wishlists',
            field=models.ManyToManyField(to='catalog.Wishlist'),
        ),
    ]
