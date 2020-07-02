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
    outer_message = models.CharField(max_length=500, null=True, blank=True)
    inner_message = models.CharField(max_length=500, null=True, blank=True)
    NO = 'None'
    LC = 'Living Coral'
    UV = 'Ultra Violet'
    GR = 'Greenery'
    RQ = 'Rose Quartz'
    SE = 'Serenity'
    MA = 'Marsala'
    RO = 'Radiand Orchid'
    EM = 'Emerald'
    TT = 'Tangerine Tango'
    HS = 'Honeysucle'
    TQ = 'Turquoise'
    MI = 'Mimosa'
    BI = 'Blue Izis'
    CP = 'Chili Pepper'
    SD = 'Sand Dollar'
    BT = 'Blue Turquoise'
    TL = 'Tigerlily'
    AS = 'Aqua Sky'
    TR = 'True Red'
    FR = 'Fuchsia Rose'
    CB = 'Cerulean Blue'
    COLOR_CHOICES = [
        (NO, 'None'),
        (LC, 'Living Coral'),
        (UV, 'Ultra Violet'),
        (GR, 'Greenery'),
        (RQ, 'Rose Quartz'),
        (SE, 'Serenity'),
        (MA, 'Marsala'),
        (RO, 'Radiand Orchid'),
        (EM, 'Emerald'),
        (TT, 'Tangerine Tango'),
        (HS, 'Honeysucle'),
        (TQ, 'Turquoise'),
        (MI, 'Mimosa'),
        (BI, 'Blue Izis'),
        (CP, 'Chili Pepper'),
        (SD, 'Sand Dollar'),
        (BT, 'Blue Turquoise'),
        (TL, 'Tigerlily'),
        (AS, 'Aqua Sky'),
        (TR, 'True Red'),
        (FR, 'Fuchsia Rose'),
        (CB, 'Cerulean Blue'),
    ]
    color = models.CharField(max_length=15, choices=COLOR_CHOICES, default=NO)
    ML = 'Montserrat + Lora (Modern)'
    PL = 'Prata + Lato (Elegant)'
    AJ = 'Archivo Black + Judson (Emphasis)'
    FONT_CHOICES = [
        (ML, 'Montserrat + Lora (Modern)'),
        (PL, 'Prata + Lato (Elegant)'),
        (AJ, 'Archivo Black + Judson (Emphasis)'),
    ]
    font = models.CharField(max_length=33, choices=FONT_CHOICES, default=ML)
    NONE = 'None'
    SOLID = 'Solid'
    INSET = 'Inset'
    BORDER_CHOICES = [
        (NONE, 'None'),
        (SOLID, 'Solid'),
        (INSET, 'Inset'),
    ]
    border = models.CharField(max_length=500, choices=BORDER_CHOICES, default=NONE)
    posted_at = models.DateTimeField(auto_now_add=True)
