from typing import Optional
from urllib.parse import urlencode

import requests
from requests.auth import HTTPBasicAuth

from django_hell_auth import settings


class AuthServer:
    def __init__(self, url: str, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.url = url
        self.authorization_endpoint = url + "oauth/authorize"
        self.token_endpoint = url + "oauth/token"

    def auth(self, redirect_uri: str, state: str, scope: str = "read_user") -> str:
        return (
            self.authorization_endpoint
            + "?"
            + urlencode(
                dict(
                    client_id=self.client_id,
                    response_type="code",
                    redirect_uri=redirect_uri,
                    state=state,
                    scope=scope,
                )
            )
        )

    def request_token(self, redirect_uri: str, code: str) -> "TokenResponse":
        client_auth = HTTPBasicAuth(self.client_id, self.client_secret)
        req_return = requests.post(
            self.token_endpoint,
            auth=client_auth,
            data=dict(
                grant_type="authorization_code",
                redirect_uri=redirect_uri,
                code=code,
            ),
        )
        req_return.raise_for_status()
        return TokenResponse(req_return.json(), self)


class TokenResponse:
    def __init__(self, data: dict[str, str], server: Optional["AuthServer"] = None):
        self._data = data

        if server:
            req_return = requests.get(
                server.url + "api/v4/user",
                params=dict(
                    access_token=self.access_token,
                ),
            )
            req_return.raise_for_status()
            data = req_return.json()
            self.client_id = {"sub": data["username"]}

    @property
    def access_token(self) -> str:
        return self._data["access_token"]


if (
    settings.GITLAB_SERVER
    and settings.GITLAB_CLIENT_ID
    and settings.GITLAB_CLIENT_SECRET
):
    auth_server = AuthServer(
        settings.GITLAB_SERVER, settings.GITLAB_CLIENT_ID, settings.GITLAB_CLIENT_SECRET
    )
