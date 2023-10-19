# trustpilot

[![Build Status](https://travis-ci.org/trustpilot/python-trustpilot.svg?branch=master)](https://travis-ci.org/trustpilot/python-trustpilot) [![Latest Version](https://img.shields.io/pypi/v/trustpilot.svg)](https://pypi.python.org/pypi/trustpilot) [![Python Support](https://img.shields.io/pypi/pyversions/trustpilot.svg)](https://pypi.python.org/pypi/trustpilot)

Python HTTP client for [Trustpilot](https://developers.trustpilot.com/).

### Features

- Extends the [`requests.Session`](http://docs.python-requests.org/en/master/api/#requests.Session) class with automatic authentication for public and private endpoints
- GET, POST, PUT, DELETE, HEAD, OPTIONS and PATCH methods are exposed on module level
- Implements session factory and default singleton session
- Provides a simple hook system
- [CLI](#CLI) tool with basic HTTP commands


## Installation

Install the package from [PyPI](http://pypi.python.org/pypi/) using [pip](https://pip.pypa.io/):

```
pip install trustpilot
```

## Usage

_(for **full usage documentation** checkout [docs](https://github.com/trustpilot/python-trustpilot/blob/master/docs/README.md))_

```python
from trustpilot import client
client.default_session.setup(
    api_host="https://api.trustpilot.com",
    api_key="YOUR_API_KEY",
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

### CLI

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

You can also supply the variables with:

**--config/-c** : As JSON config file in the following format:

```json
{
  "TRUSTPILOT_API_HOST": "foo",
  "TRUSTPILOT_API_KEY": "bar",
  "TRUSTPILOT_API_SECRET": "baz",
  "TRUSTPILOT_API_VERSION": "v1",
  "TRUSTPILOT_USERNAME": "username",
  "TRUSTPILOT_PASSWORD": "password"
}
```

or **--env/-e** : As DotEnv config file in the following format:

```ini
TRUSTPILOT_API_HOST=foo
TRUSTPILOT_API_KEY=bar
TRUSTPILOT_API_SECRET=baz
TRUSTPILOT_API_VERSION=v1
TRUSTPILOT_USERNAME=username
TRUSTPILOT_PASSWORD=password
```

## Changelog

see [HISTORY.md](https://github.com/trustpilot/python-trustpilot/blob/master/HISTORY.md)

## Issues / DEV

Report issues [here](https://github.com/trustpilot/python-trustpilot/issues) and we welcome collaboration through PullRequests :-)
