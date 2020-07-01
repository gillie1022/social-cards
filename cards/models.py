from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from users.models import User


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Card(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='cards')
    message = models.CharField(max_length=500)
    color = models.CharField(max_length=500, null=True, blank=True)
    font = models.CharField(max_length=500, null=True, blank=True)
    border = models.CharField(max_length=500, null=True, blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

class Friend(models.Model):
    pass

