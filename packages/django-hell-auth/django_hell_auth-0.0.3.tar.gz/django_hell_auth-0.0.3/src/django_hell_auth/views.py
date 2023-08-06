from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import redirect, resolve_url
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from .oidc import auth_server


@login_required
def index(_request: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the polls index.")


def login(request: HttpRequest) -> HttpResponsePermanentRedirect:
    return_path = request.GET.get(auth.REDIRECT_FIELD_NAME, "")
    url = request.build_absolute_uri(reverse("gitlab_oidc_callback"))
    print(url)
    return redirect(
        auth_server.auth(
            redirect_uri=url,
            state=return_path,
        )
    )


def callback(request: HttpRequest) -> HttpResponsePermanentRedirect:
    return_path = str(request.GET.get("state"))

    request_token = auth_server.request_token(
        redirect_uri=request.build_absolute_uri(reverse("gitlab_oidc_callback")),
        code=request.GET["code"],
    )

    user_model = auth.get_user_model()
    user, _created = user_model.objects.get_or_create(
        username=request_token.client_id["sub"]
    )
    auth.login(request, user)

    url_is_safe = url_has_allowed_host_and_scheme(
        url=return_path,
        allowed_hosts=set(request.get_host()),
        require_https=request.is_secure(),
    )
    if not url_is_safe:
        return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))
    return redirect(return_path)
