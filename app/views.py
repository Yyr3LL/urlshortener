from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView, ListView, RedirectView, TemplateView
import hashlib

from .forms import CreateShortUrl
from .models import UrlsList, Log, ShortenedUrl


class CreateUrlView(CreateView):
    template_name = 'create.html'
    form_class = CreateShortUrl

    def generate_short_url(self, url):
        hash_obj = hashlib.md5(str(url).encode('utf-8'))
        return hash_obj.hexdigest()[:8]

    def add_url_to_list(self, url):
        """
        Adds shortened url to user's urls list
        """
        url_list = UrlsList.objects.get(user_id=self.request.user)
        url_list.urls.add(url)
        url_list.save()

    def form_valid(self, form):
        long_url = form.cleaned_data['long_url']
        short_url = self.generate_short_url(long_url)

        form.instance.short_url = short_url
        form.instance.save()

        self.add_url_to_list(form.instance)

        return HttpResponseRedirect('/urls/list/')


class UrlListView(ListView):
    template_name = 'urllist.html'
    context_object_name = 'urls'

    def get_queryset(self):
        return UrlsList.objects.get(user=self.request.user).urls.all()


class StatisticsView(ListView):
    template_name = 'statistics.html'
    context_object_name = 'logs'

    def get_queryset(self):
        return Log.objects.filter()


class RedirectFromShortenedView(TemplateView):

    def create_log(self, url):
        """
        Creates log object for particular shortened url which contains:
        ip, referer and date when url was used
        """
        default_referer = 'unknown'
        referer = self.request.headers.get('Referer', default_referer)
        log_ip = ''

        if ip := self.request.META.get('HTTP_X_FORWARDED_FOR'):
            log_ip = ip
        elif ip := self.request.META.get('REMOTE_ADDR'):
            log_ip = ip

        Log.objects.create(
            url=url,
            referer=referer,
            ip=log_ip
        )

    def get(self, request, *args, **kwargs):
        url = get_object_or_404(ShortenedUrl, short_url=kwargs['short_url'])
        self.create_log(url)
        print(url.long_url)
        return HttpResponseRedirect(url.long_url)
