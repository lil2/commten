from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


PRIORITY_CHOICES = (('Python', 'Python'),
                    ('Django', 'Django'),
                    ('GitHub', 'GitHub'),
                    ('Selenium', 'Selenium'))


# Create your models here.
class User(AbstractUser):
    follows = models.ManyToManyField('self', related_name='follow_to', symmetrical=False)


class Post(models.Model):
    author = models.ForeignKey(User, related_name='posts')
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=100, choices=PRIORITY_CHOICES, default='Python')
    body = models.TextField(blank=True, null=True)
    image = models.FileField(blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now)
    publish_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.publish_date = timezone.now()
        self.save()


class Photo(models.Model):
    post = models.ForeignKey(Post, related_name='photos')
    image = models.ImageField(upload_to='%Y/%m/%d')