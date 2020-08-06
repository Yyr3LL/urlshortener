# Generated by Django 3.1 on 2020-08-06 05:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortenedUrl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_url', models.TextField()),
                ('long_url', models.TextField()),
            ],
            options={
                'verbose_name': 'Shortened url',
                'verbose_name_plural': 'Shortened urls',
            },
        ),
        migrations.CreateModel(
            name='UrlsList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('urls', models.ManyToManyField(to='app.ShortenedUrl')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='url_list', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Url list',
                'verbose_name_plural': 'Url lists',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('referer', models.TextField()),
                ('ip', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.shortenedurl', verbose_name='Statistics')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
        ),
    ]
