from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class Home(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='media/', default="media/estadia.jpeg")
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

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


class Comment(models.Model):
    home = models.ForeignKey('airbnb.Home', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.save()

    def __str__(self):
        self.approved_comment = True
        return self.text

   
class Rating(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.home.name} - {self.user}"
