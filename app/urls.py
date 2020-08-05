from django.urls import path
from .views import CreateUrlView, UrlListView

urlpatterns = [
    path('', CreateUrlView.as_view()),
    path('list/', UrlListView.as_view()),
]
