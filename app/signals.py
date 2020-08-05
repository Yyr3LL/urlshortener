from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import UrlsList, ShortenedUrl, Log


@receiver(post_save, sender=User)
def create_user_url_list(sender, instance, created, **kwargs):
    if created:
        UrlsList.objects.create(user=instance)
