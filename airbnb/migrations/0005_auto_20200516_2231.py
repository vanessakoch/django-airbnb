# Generated by Django 3.0.5 on 2020-05-17 01:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('airbnb', '0004_home_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='home',
            old_name='publish_date',
            new_name='published_date',
        ),
    ]