# Generated by Django 3.0.5 on 2020-05-22 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airbnb', '0021_auto_20200522_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=30),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='total_value',
            field=models.DecimalField(decimal_places=2, max_digits=30),
        ),
    ]
