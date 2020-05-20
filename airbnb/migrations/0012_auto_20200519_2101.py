# Generated by Django 3.0.5 on 2020-05-20 00:01

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('airbnb', '0011_auto_20200519_1740'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='stars',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterUniqueTogether(
            name='rating',
            unique_together={('user', 'home')},
        ),
        migrations.AlterIndexTogether(
            name='rating',
            index_together={('user', 'home')},
        ),
        migrations.RemoveField(
            model_name='rating',
            name='rated_on',
        ),
        migrations.RemoveField(
            model_name='rating',
            name='rating',
        ),
    ]