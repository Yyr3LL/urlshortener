from .models import UrlsList


def generate_short_url(url):
    return 'pass'


def add_url_to_list(user_id, url):
    print(user_id)
    url_list = UrlsList.objects.get(user_id=user_id)
    url_list.urls.add(url)
    url_list.save()
