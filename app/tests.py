from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse

from .views import CreateUrlView, UrlListView
from .models import ShortenedUrl


class AuthTest(TestCase):
    def test_can_signup(self):
        c = Client()
        response = c.post('/auth/signup', {
            'username': 'yy',
            'password': '123123123'
        })
        self.assertEqual(response.status_code, 301)

    def test_if_unauthorized_redirected(self):
        c = Client()
        response = c.get(reverse('create url'))
        self.assertRedirects(response, '/auth/login/?next=/', status_code=302, target_status_code=200)


class CreateUrlTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='yy', password='asdasd'
        )

    def test_is_url_created(self):
        long_url = 'https://youtube.com/'

        request = self.factory.post('/', {
            'long_url': long_url
        })

        request.user = self.user
        response = CreateUrlView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(ShortenedUrl.objects.get(pk=1).long_url, long_url)


class ListUrlTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='yy', password='asdasd'
        )

    def test_is_url_created(self):
        long_url = 'https://youtube.com/'

        request = self.factory.post('/', {
            'long_url': long_url
        })

        request.user = self.user
        response = CreateUrlView.as_view()(request)

        request = self.factory.get('/list')
        request.user = self.user

        response = UrlListView.as_view()(request)

        self.assertEqual(response.status_code, 200)
