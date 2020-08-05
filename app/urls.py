from django.conf.urls import url
from django.urls import path, re_path
from .views import CreateUrlView, UrlListView, RedirectFromShortenedView, StatisticsView

urlpatterns = [
    path('', CreateUrlView.as_view(), name='create url'),
    path('list/', UrlListView.as_view(), name='list urls'),
    url(r'^(?P<short_url>\w{8})$', RedirectFromShortenedView.as_view(), name='redirect')
]
