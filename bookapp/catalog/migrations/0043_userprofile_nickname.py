# Generated by Django 3.0.3 on 2020-03-29 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0042_bookrating_anonymous'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='nickname',
            field=models.CharField(default='', max_length=10),
        ),
    ]