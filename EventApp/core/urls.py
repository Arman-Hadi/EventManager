from os import environ

from django.urls import path

from .views import webhook


urlpatterns = [
    path(f'hook_{environ.get("HOOK_UUID")}', webhook, name='webhook'),
]
