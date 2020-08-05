from django.contrib.auth.models import User
from django.db import models


class ShortenedUrl(models.Model):
    short_url = models.TextField()
    long_url = models.TextField()

    class Meta:
        verbose_name = 'Shortened url'
        verbose_name_plural = 'Shortened urls'


class UrlsList(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='url_list'
    )
    urls = models.ManyToManyField(
        ShortenedUrl
    )

    class Meta:
        verbose_name = 'Url list'
        verbose_name_plural = 'Url lists'


class Log(models.Model):
    url = models.ForeignKey(
        ShortenedUrl,
        verbose_name='Statistics',
        on_delete=models.CASCADE
    )
    referer = models.TextField()
    ip = models.TextField()
    date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
