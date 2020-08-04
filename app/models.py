from django.db import models


class ShortenedUrl(models.Model):
    short_url = models.TextField()
    long_url = models.TextField()

    class Meta:
        verbose_name = 'Shortened url'
        verbose_name_plural = 'Shortened urls'


class UrlsList(models.Model):
    shortened_url = models.ManyToManyField(
        ShortenedUrl
    )

    class Meta:
        verbose_name = 'Url list'
        verbose_name_plural = 'Url lists'


class Log(models.Model):
    statistics = models.OneToOneField(
        ShortenedUrl,
        verbose_name='Statistics',
        on_delete=models.CASCADE
    )
    referer = models.TextField()
    ip = models.TextField()
    date = models.DateField()

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
