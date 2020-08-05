from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, ListView, TemplateView
import hashlib

from .forms import CreateShortUrl
from .models import UrlsList, Log, ShortenedUrl


class CreateUrlView(LoginRequiredMixin, CreateView):
    login_url = '/auth/login/'
    template_name = 'create.html'
    login_required = True
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

        return redirect(reverse('list urls'))


class UrlListView(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    template_name = 'urllist.html'
    context_object_name = 'urls'

    def get_queryset(self):
        return UrlsList.objects.get(user=self.request.user).urls.all()


class StatisticsView(LoginRequiredMixin, ListView):
    login_url = '/auth/login/'
    template_name = 'statistics.html'
    context_object_name = 'logs'

    def get_queryset(self, **kwargs):
        return Log.objects.filter(url__short_url=self.kwargs['short_url'])


class RedirectFromShortenedView(LoginRequiredMixin, TemplateView):

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
        return redirect(url.long_url)
