from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, ListView

from .forms import CreateShortUrl
from .models import UrlsList
from .service import generate_short_url, add_url_to_list


class CreateUrlView(CreateView):
    template_name = 'create.html'
    form_class = CreateShortUrl

    def form_valid(self, form):
        long_url = form.cleaned_data['long_url']
        short_url = generate_short_url(long_url)

        form.instance.short_url = short_url
        form.instance.save()

        print(self.request.user)
        print(self.request.user.id)
        add_url_to_list(self.request.user.id, form.instance)

        return HttpResponseRedirect('/zdarova')


class UrlListView(ListView):
    template_name = 'urllist.html'
    context_object_name = 'urls'

    def get_queryset(self):
        print(self.request.user.id)
        return UrlsList.objects.get(user=self.request.user).urls.all()
