from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save



PRIORITY_CHOICES = (('Maintenance', 'Maintenance'),
                    ('Billing', 'Billing'),
                    ('Other', 'Other'))


# Create your models here.
class User(AbstractUser):
    follows = models.ManyToManyField('self', related_name='follow_to', symmetrical=False, blank=True)


class Tickets(models.Model):
    author = models.ForeignKey(User, related_name='posts')
    status = models.BooleanField(default=True)
    title = models.CharField(max_length=50)
    type = models.CharField(max_length=100, choices=PRIORITY_CHOICES, default='Maintenance')
    body = models.TextField(blank=True, null=True)
    image = models.FileField(blank=True, null=True)
    create_date = models.DateTimeField(default=timezone.now)
    publish_date = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return str(self.author)

    def publish(self):
        self.publish_date = timezone.now()
        self.save()


class Photo(models.Model):
    post = models.ForeignKey(Tickets, related_name='photos')
    image = models.ImageField(upload_to='%Y/%m/%d')



class Comment(models.Model):
    # related_name for accessing comment from post model
    post = models.ForeignKey('commten.Tickets', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.text


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user')
    phone = models.CharField(max_length=20, blank=True, default='')
    address = models.CharField(max_length=100, default='', blank=True)
    apt = models.CharField(max_length=100, default='', blank=True)
    city = models.CharField(max_length=100, default='', blank=True)
    state = models.CharField(max_length=100, default='', blank=True)
    zipcode = models.CharField(max_length=100, default='', blank=True)
    def __str__(self):
        return str(self.user)

def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()
post_save.connect(create_profile, sender=User)
