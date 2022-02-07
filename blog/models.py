from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=250)
    brief_description = models.CharField(max_length=250)
    full_description = models.CharField(max_length=500)
    image = models.ImageField(null=True, blank=True)
    posted = models.BooleanField(default=False)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class Comment(models.Model):
    username = models.CharField(max_length=250, default='Niko')
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    posted_com = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class UserUrl(User):

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.pk})

