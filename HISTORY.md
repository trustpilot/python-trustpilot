## History

### 0.1.0 (2016-11-09)

- First release on gemfury

### 0.1.1 (2016-11-09)

- change names

### 0.1.2 (2016-11-09)

- fix issue with 401-retry

### 0.1.3 (2016-11-10)

- add dependencies to setup.py

### 0.1.4 (2016-11-11)

- cli tool

### 0.1.5 (2016-11-11)

- fix apikey url query param error

### 0.1.6 (2016-11-11)

- introduce different token_issuer_host thatn api_host

### 0.1.7 (2016-12-06)

- Introduce context_getter on session object, defaulted to holding
  CorrelationId=random_uuid

### 1.0.0 (2017-02-01)

- first release as oss, major refactoring of inner machinery (session
  objects, retry policies, cli, tests etc)

### 1.1.0 (2017-06-12)

- fixed logging so it does not use root logger. according to best
  practices mentioned in
  <http://pythonsweetness.tumblr.com/post/67394619015/use-of-logging-package-from-within-a-library>
- removed dependency on httpretty since it is not supporting py3

### 2.0.0 (2017-09-29)

- DEPRECATED: create_session is getting deprecated, use
  trustpilot.client.default_session.setup instead
- now able to query public endpoints without being authenticated

### 2.1.0 (2017-10-05)

- fixed issue in cli.post & cli.put where 'content_type' should be
  'content-type'

### 3.0.0 (2018-01-18)

DELETED DO NOT USE\!\!

- add async-client

### 3.0.1 (2018-01-18)

- removed prints
- made async_client retry on unauthorized

### 4.0.0 (2018-06-06)

- drop support for Python 3.3

### 4.0.1 (2018-06-06)

- Switch to non-deprecated session object for utility method calls

### 4.0.2 (2018-10-30)

- Upgrade requests to 2.20.0

### 5.0.0 (2019-01-04)

- Update to authentication methods

### 5.0.1 (2019-02-04)

- Fix documentation formatting

### 6.0.0 (2019-02-06)

- reorganize code
- add user-agent header
- get access_token with async call in async_client

### 6.0.3 (2019-08-15)

- Added support for 'API Version' parameter for Client initialisation.

### 6.0.4 (2019-08-15)

- Remove auto-deploy to travis

### 6.0.5 (2019-08-15)

- allow newer version of requests dependency

### 6.0.6 (2019-09-18)

- specify user agent through env-var or kwarg

### 6.0.8 (2019-09-19)

- pass user_agent property down to session correctly
- handle duplicate api version properly

### 6.0.9 (2019-09-19)

- fix: transmit user-agent on all requests

### 6.0.10 (2019-09-20)

- fix: handle duplicate api version for both sync and async clients

### 6.1.0 (2020-01-06)

- dependencies: github security upgrade of requests and urllib

### 7.0.0 (2020-01-13)

**breaking changes**:

- python 2.7 support now gone since it reached end of-life
- now only supporting async_client for 3.6+
- now depending on async_generator for asynccontextmanager support in 3.6+

**new features**:

- advanced mode using the **request_context_manager** directly

### 7.0.1 (2020-01-13)

- add shortcut to singleton async request_context_manager

### 8.0.0 (2020-03-25)

- update click to version 7.1.1 which renames the command `create_access_token` to `create-access-token`
- drop support for python 3.6
- drop deprecated `trustpilot.client.get_session` method. It is replaced by `trustpilot.client.default_session`
- drop deprecated `trustpilot.client.create_session` method. it is replaced by `trustpilot.client.default_session.setup`

### 8.0.1 (2020-03-26)

- create new patch version to fix travis

### 8.1.0 (2020-04-15)

- reintroduce cli script

### 9.0.0 (2020-04-29)

- username/passwrd are now optional
- dot-env support in cli
- `patch` command exposed in cli
- output format can now be `raw` or `json`, (default=json)

### 10.0.0 (2023-07-28)

- bumps versions of dependencies:
  - `python`: 3.7 → 3.8
  - `click`: 7.1.1 → 8.0.1
  - `requests`: 2.23.0 → 2.31.0
  - `aiohttp`: 3.6.2 → 3.8.5

- bumps versions of development dependencies:
  - `responses`: 0.10.12 → 0.23.2
  - `mock`: 4.0.2 → 5.1.0
  - `pytest`: 5.4.1 → 7.4.0
  - `aioresponses`: 0.6.3 → 0.7.4
  - `black`: 19.10b0 → 23.7.0
