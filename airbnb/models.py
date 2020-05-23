from django.conf import settings
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

class Address(models.Model):
    estado = [
           ('AC', 'Acre'),
           ('AL', 'Alagoas'),
           ('AP', 'Amapá'),
           ('AM', 'Amazonas'),
           ('BA', 'Bahia'),
           ('CE', 'Ceará'),
           ('DF', 'Distrito Federal'),
           ('ES', 'Espírito Santo'),
           ('GO', 'Goiás'),
           ('MA', 'Maranhão'),
           ('MT', 'Mato Grosso'),
           ('MS', 'Mato Grosso do Sul'),
           ('MG', 'Minas Gerais'),
           ('PA', 'Pará'),
           ('PB', 'Paraíba'),
           ('PR', 'Paraná'),
           ('PE', 'Pernambuco'),
           ('PI', 'Piauí'),
           ('RJ', 'Rio de Janeiro'),
           ('RS', 'Rio Grande do Sul'),
           ('RO', 'Rondônia'),
           ('RR', 'Roraima'),
           ('SC', 'Santa Catarina'),
           ('SP', 'São Paulo'),
           ('SE', 'Sergipe'),
           ('TO', 'Tocantins'),
           ]

    country = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    state = models.CharField(max_length=60, choices=estado)
    city = models.CharField(max_length=60) 
    street = models.CharField(max_length=100)
    phone = models.IntegerField()

    def __str__(self):
        return f"{self.street} - {self.city} ({self.state}) - {self.country} CEP: {self.zipcode} - Contato: {self.phone} "

class Home(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', default="media/estadia.jpeg")
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=30, decimal_places=2)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

    def no_of_ratings(self):
        return Rating.objects.filter(home=self).count()

    def avg_rating(self):
        total = 0
        ratings = Rating.objects.filter(home=self)
        for rating in ratings:
            total += rating.stars
        if len(ratings) > 0:
            return total/len(ratings)
        else:
            return 0

class Rating(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.home.name} - {self.user}"

class Reserve(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    initial_date = models.DateField()
    final_date = models.DateField()
    number_peoples = models.IntegerField()
    total_value = models.DecimalField(max_digits=30, decimal_places=2)

    def __str__(self):
        return str(self.total_value)

class Search(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    local = models.CharField(max_length=20)
    number_of_days = models.IntegerField()
    number_of_peoples = models.IntegerField()
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.local} - {self.number_of_days} - {self.number_of_peoples}"

class Comment(models.Model):
    home = models.ForeignKey('airbnb.Home', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
   
