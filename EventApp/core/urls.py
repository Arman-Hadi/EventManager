from os import environ, getenv

from django.urls import path

from .views import webhook


urlpatterns = [
    path(f'hook_{getenv("HOOK_UUID")}', webhook, name='webhook'),
]
