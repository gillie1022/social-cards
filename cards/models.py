from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.db.models import Q
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from users.models import User

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Card(models.Model):
    author = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='cards')
    outer_message = models.CharField(max_length=500, null=True, blank=True)
    inner_message = models.CharField(max_length=500, null=True, blank=True)
    
    COLOR_CHOICES = (
        ('None', 'None'),
        ('Living Coral', 'Living Coral'),
        ('Ultra Violet', 'Ultra Violet'),
        ('Greenery', 'Greenery'),
        ('Rose Quartz', 'Rose Quartz'),
        ('Serenity', 'Serenity'),
        ('Marsala', 'Marsala'),
        ('Radiand Orchid', 'Radiand Orchid'),
        ('Emerald', 'Emerald'),
        ('Tangerine Tango', 'Tangerine Tango'),
        ('Honeysucle', 'Honeysucle'),
        ('Turquoise', 'Turquoise'),
        ('Mimosa', 'Mimosa'),
        ('Blue Izis', 'Blue Izis'),
        ('Chili Pepper', 'Chili Pepper'),
        ('Sand Dollar', 'Sand Dollar'),
        ('Blue Turquoise', 'Blue Turquoise'),
        ('Tigerlily', 'Tigerlily'),
        ('Aqua Sky', 'Aqua Sky'),
        ('True Red', 'True Red'),
        ('Fuchsia Rose', 'Fuchsia Rose'),
        ('Cerulean Blue', 'Cerulean Blue'),
    )
    color = models.CharField(max_length=15, choices=COLOR_CHOICES, default='None')
    
    FONT_CHOICES = (
        ('Montserrat + Lora (Modern)', 'Montserrat + Lora (Modern)'),
        ('Prata + Lato (Elegant)', 'Prata + Lato (Elegant)'),
        ('Archivo Black + Judson (Emphasis)', 'Archivo Black + Judson (Emphasis)'),
    )
    font = models.CharField(max_length=33, choices=FONT_CHOICES, default='Montserrat + Lora (Modern)')
    
    BORDER_CHOICES = (
        ('None', 'None'),
        ('Solid', 'Solid'),
        ('Inset', 'Inset'),
    )
    border = models.CharField(max_length=500, choices=BORDER_CHOICES, default='None')
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_at']
