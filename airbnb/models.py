from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Home(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.FileField(upload_to="%Y/%m/%d/", default="img/estadia.jpeg")
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(default=0)
    creation_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.name