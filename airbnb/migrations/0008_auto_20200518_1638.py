# Generated by Django 3.0.5 on 2020-05-18 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airbnb', '0007_auto_20200517_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='home',
            name='image',
            field=models.ImageField(default='media/estadia.jpeg', upload_to='media/'),
        ),
    ]