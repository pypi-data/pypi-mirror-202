from django.urls import re_path

from .views import callback, login

app_name = "django-hell-auth"  # pylint: disable=invalid-name
urlpatterns = [
    re_path(r"^$", login, name="login"),
    re_path(r"^callback/$", callback, name="callback"),
]
