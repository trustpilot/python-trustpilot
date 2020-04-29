# Usage

Complete instructions for how to use the **Trustpilot** module and `trustpilot_api_client` commandline tool.

## Installation

Install the package from [PyPI](http://pypi.python.org/pypi/) using [pip](https://pip.pypa.io/):

```
pip install trustpilot
```

## Getting Started

This client is using the [Requests](http://docs.python-requests.org/en/master/) library. Responses are standard [`requests.Response`](http://docs.python-requests.org/en/master/api/#requests.Response) objects. You can use it as a factory or as a singleton.

### Use the singleton session

Use the built-in `default session` to instantiate a globally accessible session.

```python
from trustpilot import client
client.default_session.setup(
    api_host="https://api.trustpilot.com",  # optional, default: https://api.tp-staging.com
    api_version="v1",  # optional, default: v1
    api_key="YOUR_API_KEY",  # required
    api_secret="YOUR_API_SECRET",  #  optional
    username="YOUR_TRUSTPILOT_BUSINESS_USERNAME",  # optional
    password="YOUR_TRUSTPILOT_BUSINESS_PASSWORD"  # optional
)
response = client.get("/foo/bar")
status_code = response.status_code

```

You can rely on environment variables for the setup of sessions so

```bash
$ env
TRUSTPILOT_API_HOST=https://api.trustpilot.com
TRUSTPILOT_API_KEY=foo
TRUSTPILOT_API_SECRET=bar
```

> optionally supply:
> ```ini
> TRUSTPILOT_API_VERSION=v1
> TRUSTPILOT_USERNAME=username
> TRUSTPILOT_PASSWORD=password
> ```

Will work with the implicit `default_session` and the `TrustpilotSession.setup` method.

```python
from trustpilot import client
client.get("/foo/bar")
```

### Instantiate your own session

You can create as many sessions as you like, as long as you pass them around yourself.

```python
from trustpilot import client
session = client.TrustpilotSession(
    api_host="https://api.trustpilot.com",
    api_version="v1",
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
    username="YOUR_TRUSTPILOT_BUSINESS_USERNAME",
    password="YOUR_TRUSTPILOT_BUSINESS_PASSWORD"
)
response = session.get("/foo/bar")
```

## Async client

Since version `3.0.0` you are able to use the `async_client` for `asyncio` usecases. 
The `async_client` uses [aiohttp](https://docs.aiohttp.org/en/stable/) read here for the signarue of its [request](https://docs.aiohttp.org/en/stable/client_reference.html#aiohttp.ClientSession.request) and [response](https://docs.aiohttp.org/en/stable/client_reference.html#response-object)

To use the default `async_client` session, using `env-vars` for settings, import is as following:

```python
import asyncio
from trustpilot import async_client
loop = asyncio.get_event_loop()

async def get_response():
    response = await async_client.get('/foo/bar')
    response_json = await response.json()
    status_code = response.status

loop.run_until_complete(get_response())
```

Or instantiate the session yourself with:

```python
import asyncio
from trustpilot import async_client
loop = asyncio.get_event_loop()

session = async_client.TrustpilotAsyncSession(
    api_host="https://api.trustpilot.com", 
    api_version="v1", # optional
    api_key="YOUR_API_KEY",
    api_secret="YOUR_API_SECRET",
    username="YOUR_TRUSTPILOT_BUSINESS_USERNAME", # optional
    password="YOUR_TRUSTPILOT_BUSINESS_PASSWORD" # optional
)

async def get_response():
    response = await session.get('/foo/bar')
    response_json = await response.json()

loop.run_until_complete(get_response())
```

### Advanced async usage

The async client uses an _asynccontextmanager_ under the hood to perform the supported request methods.
A side effect of the implementation is that it buffers up all the content before returning it to the calling scope.

You can get around this limitation by using the _asynccontextmanager_ directly like in the next example.

**Example with stream reading the raw aiohttp response object:**

```
import asyncio
from trustpilot import async_client
loop = asyncio.get_event_loop()

async def get_response():
    async with session.request_context_manager('get', "/v1/foo/bar") as resp:
        result = True
        while True:
            chunk = resp.content.read(8)
            if not chunk:
                break
            result += chunk
    return result

loop.run_until_complete(get_response())
```

## Setup User Agent

A UserAgent header can be specified in two ways:

1. By populating the `TRUSTPILOT_USER_AGENT` environment var
2. By creating your own (async/sync)-client instance, or calling `setup` on the `default_session`, and supplying the kwargs `user_agent=foobar`

If no user-agent is given it will autopopulate using the function in `get_user_agent` function in [auth.py](./trustpilot/auth.py)

## CLI

The `trustpilot_api_client` command is bundled with the install

```bash
Usage: trustpilot_api_client [OPTIONS] COMMAND [ARGS]...

Options:
  --host TEXT                     Host name
  --version TEXT                  Api version
  --key TEXT                      Api key
  --secret TEXT                   Api secret
  --token_issuer_host TEXT        Token issuer host name
  --username TEXT                 Trustpilot username
  --password TEXT                 Trustpilot password
  -c, --config FILENAME           Json config file name
  -e, --env FILENAME              Dot env file
  -of, --outputformat [json|raw]  Output format, default=json
  -v, --verbose                   Verbosity level
  --help                          Show this message and exit.

Commands:
  create-access-token  Get an access token
  delete               Send a DELETE request
  get                  Send a GET request
  post                 Send a POST request with specified data
  put                  Send a PUT request with specified data
```

You can also supply the variables through with:

**--config/-c** : As JSON config file in the following format:

```json
{
  "TRUSTPILOT_API_HOST": "foo",
  "TRUSTPILOT_API_VERSION": "v1",
  "TRUSTPILOT_API_KEY": "bar",
  "TRUSTPILOT_API_SECRET": "baz",
  "TRUSTPILOT_USERNAME": "username",
  "TRUSTPILOT_PASSWORD": "password"
}
```

**--env/-e** : As DotEnv config file in the following format:

```ini
TRUSTPILOT_API_HOST=foo
TRUSTPILOT_API_VERSION=v1
TRUSTPILOT_API_KEY=bar
TRUSTPILOT_API_SECRET=baz
TRUSTPILOT_USERNAME=username
TRUSTPILOT_PASSWORD=password
```