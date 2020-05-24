# Generated by Django 3.0.5 on 2020-05-24 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airbnb', '0024_search_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=60, verbose_name='Município'),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(max_length=100, verbose_name='País'),
        ),
        migrations.AlterField(
            model_name='address',
            name='phone',
            field=models.IntegerField(verbose_name='Telefone'),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], max_length=60, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(max_length=100, verbose_name='Rua / Avenida'),
        ),
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.IntegerField(verbose_name='CEP'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(max_length=200, verbose_name='Autor'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='Texto'),
        ),
        migrations.AlterField(
            model_name='home',
            name='description',
            field=models.TextField(verbose_name='Descrição'),
        ),
        migrations.AlterField(
            model_name='home',
            name='image',
            field=models.ImageField(default='media/estadia.jpeg', upload_to='media/', verbose_name='Fotografia'),
        ),
        migrations.AlterField(
            model_name='home',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Nome do estabelecimento'),
        ),
        migrations.AlterField(
            model_name='home',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=30, verbose_name='Preço da diária'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='final_date',
            field=models.DateField(help_text='Use o formato dd/mm/AAAA', verbose_name='Data de saída'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='initial_date',
            field=models.DateField(help_text='Use o formato dd/mm/AAAA', verbose_name='Data de entrada'),
        ),
        migrations.AlterField(
            model_name='reserve',
            name='number_peoples',
            field=models.IntegerField(verbose_name='Número de pessoas'),
        ),
    ]
