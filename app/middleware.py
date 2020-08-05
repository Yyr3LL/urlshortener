from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


class AuthRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.user.is_authenticated:
            return redirect(reverse('account_login')) # or http response


        response = self.get_response(request)

        return response
