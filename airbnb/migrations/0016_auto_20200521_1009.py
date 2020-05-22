# Generated by Django 3.0.5 on 2020-05-21 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('airbnb', '0015_auto_20200521_0906'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='home',
            name='city',
        ),
        migrations.RemoveField(
            model_name='home',
            name='state',
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=100)),
                ('state', models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=60)),
                ('city', models.CharField(max_length=60)),
                ('street', models.CharField(max_length=300)),
                ('phone', models.CharField(max_length=50)),
                ('home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='airbnb.Home')),
            ],
        ),
    ]