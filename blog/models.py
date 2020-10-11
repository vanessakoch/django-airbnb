from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name="Título")
    text = models.TextField(verbose_name="Texto")
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    views = models.BigIntegerField(default=0, verbose_name="Visualizações")

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def likes_count(self):
        return PostLike.objects.filter(post=self).count()

    def dislikes_count(self):
        return PostDislike.objects.filter(post=self).count()

    def __str__(self):
        return self.title

    def approved_comments(self):
        return self.comments.filter(approved_comment=True)

class PostLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.post.title, self.user)

class PostDislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} - {}'.format(self.post.title, self.user)

class PostComment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200, verbose_name="Autor")
    text = models.TextField(verbose_name="Texto")
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text
