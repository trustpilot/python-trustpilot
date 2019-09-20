# pylint: disable-all
import pytest
import sys
from aioresponses import aioresponses
import asyncio
from trustpilot import async_client

@pytest.mark.skipif(
    sys.version_info < (3, 5, 2), reason="requires python 3.5.2 or above"
)
def test_async_client_auth_and_get():
    loop = asyncio.get_event_loop()

    with aioresponses() as m:
        m.get("https://api.tp-staging.com/v1/foo/bar", status=401)
        m.post(
            "https://api.tp-staging.com/v1/oauth/oauth-business-users-for-applications/accesstoken",
            payload=dict(access_token="foobarbaz"),
        )
        m.get("https://api.tp-staging.com/v1/foo/bar", payload=dict(foo="foobarbaz"))

        session = async_client.TrustpilotAsyncSession(
            api_host="https://api.tp-staging.com",
            api_key="something",
            api_secret="secret",
            username="username",
            password="password",
            api_version="v1",
        )

        async def get_response():
            response = await session.get("/foo/bar")
            response_json = await response.json()
            assert response_json["foo"] == "foobarbaz"
            assert session.access_token == "foobarbaz"

        resp = loop.run_until_complete(get_response())


@pytest.mark.skipif(
    sys.version_info < (3, 5, 2), reason="requires python 3.5.2 or above"
)
def test_async_api_version():
    loop = asyncio.get_event_loop()

    with aioresponses() as m:
        m.get("https://api.tp-staging.com/v1/foo/bar", status=200)
        m.get("https://api.tp-staging.com/v1/v2/foo/bar", status=404)
        m.get("https://12345.com/v23/foo/bar", status=200)

        session = async_client.TrustpilotAsyncSession(
            api_host="https://api.tp-staging.com",
            api_key="something",
            api_secret="secret",
            username="username",
            password="password",
            api_version="v1",
        )

        async def get_response():
            res = await session.get("/v1/foo/bar")
            double_res = await session.get("/v2/foo/bar")
            full_url_res = await session.get("https://12345.com/v23/foo/bar")

            assert res.status == 200
            assert double_res.status == 404
            assert full_url_res.status == 200

        resp = loop.run_until_complete(get_response())