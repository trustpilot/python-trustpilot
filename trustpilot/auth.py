import requests
import base64
import logging
import platform
from trustpilot import VERSION

OS = platform.system()
PYTHON_VERSION = platform.python_version()
SCOPE = "external"


def get_user_agent():
    user_agent = "python-trustpilot-client?scope={scope}&version={version}&python-version={python_version}&os={os}".format(
        scope=SCOPE, version=VERSION, python_version=PYTHON_VERSION, os=OS
    )
    return user_agent


def create_access_token_request_params(session):
    url = "{token_issuer_host}/{api_version}/{token_issuer_path}".format(
        token_issuer_host=session.token_issuer_host.rstrip("/"),
        api_version=session.api_version.rstrip("/"),
        token_issuer_path=session.token_issuer_path,
    )

    data = {
        'grant_type': 'client_credentials'
        }

    if session.username and session.password:
        data = {
            "grant_type": "password",
            "username": session.username,
            "password": session.password,
        }

    headers = {
        "Authorization": "Basic {}".format(
            base64.b64encode(
                (session.api_key + ":" + session.api_secret).encode("ascii")
            ).decode("ascii")
        ),
        "User-Agent": session.user_agent,
    }

    return url, data, headers
