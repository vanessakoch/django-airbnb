# Generated by Django 3.0.5 on 2020-05-22 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airbnb', '0020_reserve_total_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserve',
            name='total_value',
            field=models.FloatField(default=0),
        ),
    ]
