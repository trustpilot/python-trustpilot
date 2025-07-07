import json
from click.testing import CliRunner

try:
    from unittest import mock
except ImportError:
    import mock
import unittest


from trustpilot.cli import cli


_creds_list = [
    "--host",
    "http://hostname",
    "--key",
    "secret_key",
    "--secret",
    "secret_secret",
    "--username",
    "username",
    "--password",
    "password",
]


class TestCliMethodsJsonOutput(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        response_mock = mock.Mock()
        response_mock.url = "https://api.trustpilot.com/v1/business-units/5400267300006400057a0113/reviews"
        response_mock.status_code = 401
        response_mock.headers = {
            "Access-Control-Allow-Headers": "Authorization, Accept, Accept-Charset, Accept-Encoding, Accept-Language, Cache-Control, Connection, Content-Length, Content-Type, Host, Origin, User-Agent, ApiKey, X-Requested-With",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Max-Age": "3628800",
            "Content-Type": "application/json",
            "Date": "Mon, 30 Jan 2017 08:59:49 GMT",
            "Server": "Apigee Router",
            "Content-Length": "90",
            "Connection": "keep-alive",
        }
        response_mock.json.return_value = {
            "fault": {
                "faultstring": "Invalid ApiKey",
                "detail": {"errorcode": "oauth.v2.InvalidApiKey"},
            }
        }
        self.response_mock = response_mock
        self.expected_output = """{
          "url": "https://api.trustpilot.com/v1/business-units/5400267300006400057a0113/reviews",
          "status": 401,
          "content": {
            "fault": {
              "faultstring": "Invalid ApiKey",
              "detail": {
                "errorcode": "oauth.v2.InvalidApiKey"
              }
            }
          }
        }
        """
        self.expected_verbose_output = """{
          "url": "https://api.trustpilot.com/v1/business-units/5400267300006400057a0113/reviews",
          "status": 401,
          "headers": {
            "Content-Length": "90",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Max-Age": "3628800",
            "Date": "Mon, 30 Jan 2017 08:59:49 GMT",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Authorization, Accept, Accept-Charset, Accept-Encoding, Accept-Language, Cache-Control, Connection, Content-Length, Content-Type, Host, Origin, User-Agent, ApiKey, X-Requested-With",
            "Content-Type": "application/json",
            "Connection": "keep-alive",
            "Server": "Apigee Router"
          },
          "content": {
            "fault": {
              "faultstring": "Invalid ApiKey",
              "detail": {
                "errorcode": "oauth.v2.InvalidApiKey"
              }
            }
          }
        }
        """

    def assert_output_equal(self, output, expected_output):
        output = "".join(output.split())
        expected_output = "".join(expected_output.split())
        try:
            output = json.loads(output)
            expected_output = json.loads(expected_output)
        except ValueError:
            pass
        assert output == expected_output

    @mock.patch("trustpilot.cli.client", autospec=True)
    def test_create_access_token(self, client_mock):
        client_mock.default_session.access_token = "access_token"
        result = self.runner.invoke(cli, _creds_list + ["create-access-token"])
        self.assert_output_equal(result.output, "access_token")

    @mock.patch("trustpilot.cli.client", autospec=True)
    @mock.patch("trustpilot.cli.auth")
    def test_no_verbosity_with_get(self, auth_mock, client_mock):
        client_mock.get.return_value = self.response_mock

        result = self.runner.invoke(
            cli,
            _creds_list
            + ["get", "/v1/business-units/5400267300006400057a0113/reviews"],
        )

        self.assert_output_equal(result.output, self.expected_output)

    @mock.patch("trustpilot.cli.client", autospec=True)
    @mock.patch("trustpilot.cli.auth")
    def test_low_verbosity_with_get(self, auth_mock, client_mock):
        client_mock.get.return_value = self.response_mock

        result = self.runner.invoke(
            cli,
            _creds_list
            + ["-v", "get", "/v1/business-units/5400267300006400057a0113/reviews"],
        )
        self.assert_output_equal(result.output, self.expected_verbose_output)

    @mock.patch("trustpilot.cli.client", autospec=True)
    @mock.patch("trustpilot.cli.auth")
    def test_no_verbosity_with_post(self, auth_mock, client_mock):
        client_mock.post.return_value = self.response_mock

        result = self.runner.invoke(
            cli,
            _creds_list
            + [
                "post",
                "/v1/business-units/5400267300006400057a0113/reviews",
                "--data",
                '{"foo": "bar"}',
                "--content_type",
                "application/json",
            ],
        )
        self.assert_output_equal(result.output, self.expected_output)

    @mock.patch("trustpilot.cli.client", autospec=True)
    @mock.patch("trustpilot.cli.auth")
    def test_no_verbosity_with_put(self, auth_mock, client_mock):
        client_mock.put.return_value = self.response_mock

        result = self.runner.invoke(
            cli,
            _creds_list
            + [
                "put",
                "/v1/business-units/5400267300006400057a0113/reviews",
                "--data",
                '{"foo": "bar"}',
                "--content_type",
                "application/json",
            ],
        )
        self.assert_output_equal(result.output, self.expected_output)

    @mock.patch("trustpilot.cli.client", autospec=True)
    @mock.patch("trustpilot.cli.auth")
    def test_no_verbosity_with_delete(self, auth_mock, client_mock):
        client_mock.delete.return_value = self.response_mock

        result = self.runner.invoke(
            cli,
            _creds_list
            + ["delete", "/v1/business-units/5400267300006400057a0113/reviews"],
        )

        self.assert_output_equal(result.output, self.expected_output)


class TestCliMethodsRawOutput(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()
        response_mock = mock.Mock()
        response_mock.url = "https://api.trustpilot.com/v1/business-units/5400267300006400057a0113/reviews"
        response_mock.status_code = 401
        response_mock.headers = {
            "Access-Control-Allow-Headers": "Authorization, Accept, Accept-Charset, Accept-Encoding, Accept-Language, Cache-Control, Connection, Content-Length, Content-Type, Host, Origin, User-Agent, ApiKey, X-Requested-With",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Max-Age": "3628800",
            "Content-Type": "application/json",
            "Date": "Mon, 30 Jan 2017 08:59:49 GMT",
            "Server": "Apigee Router",
            "Content-Length": "90",
            "Connection": "keep-alive",
        }
        response_mock.text = "\n".join(["index,name,age", "0,john,32", "1,pjerot,47"])
        self.response_mock = response_mock
        self.expected_output = "\n".join(
            [
                "url",
                "https://api.trustpilot.com/v1/business-units/5400267300006400057a0113/reviews",
                "",
                "",
                "status",
                "401",
                "",
                "",
                "content",
                "index,name,age",
                "0,john,32",
                "1,pjerot,47",
                "",
            ]
        )
        self.expected_verbose_output = "\n".join(
            [
                "url",
                "https://api.trustpilot.com/v1/business-units/5400267300006400057a0113/reviews",
                "",
                "",
                "status",
                "401",
                "",
                "",
                "headers.Access-Control-Allow-Headers",
                "Authorization, Accept, Accept-Charset, Accept-Encoding, Accept-Language, Cache-Control, Connection, Content-Length, Content-Type, Host, Origin, User-Agent, ApiKey, X-Requested-With",
                "",
                "",
                "headers.Access-Control-Allow-Methods",
                "GET",
                "",
                "",
                "headers.Access-Control-Allow-Origin",
                "*",
                "",
                "",
                "headers.Access-Control-Max-Age",
                "3628800",
                "",
                "",
                "headers.Content-Type",
                "application/json",
                "",
                "",
                "headers.Date",
                "Mon, 30 Jan 2017 08:59:49 GMT",
                "",
                "",
                "headers.Server",
                "Apigee Router",
                "",
                "",
                "headers.Content-Length",
                "90",
                "",
                "",
                "headers.Connection",
                "keep-alive",
                "",
                "",
                "content",
                "index,name,age",
                "0,john,32",
                "1,pjerot,47",
                "",
            ]
        )

    def assert_output_equal(self, output, expected_output):
        expected_output = "\n".join(expected_output.split())
        assert output == expected_output

    @mock.patch("trustpilot.cli.client", autospec=True)
    @mock.patch("trustpilot.cli.auth")
    def test_no_verbosity_with_get(self, auth_mock, client_mock):
        client_mock.get.return_value = self.response_mock

        result = self.runner.invoke(
            cli,
            _creds_list
            + [
                "-of",
                "raw",
                "get",
                "/v1/business-units/5400267300006400057a0113/reviews",
            ],
        )
        print(result.output.splitlines())
        assert result.output == self.expected_output

    @mock.patch("trustpilot.cli.client", autospec=True)
    @mock.patch("trustpilot.cli.auth")
    def test_low_verbosity_with_get(self, auth_mock, client_mock):
        client_mock.get.return_value = self.response_mock

        result = self.runner.invoke(
            cli,
            _creds_list
            + [
                "-of",
                "raw",
                "-v",
                "get",
                "/v1/business-units/5400267300006400057a0113/reviews",
            ],
        )
        print(result.output)
        assert result.output == self.expected_verbose_output

    @mock.patch("trustpilot.cli.client", autospec=True)
    @mock.patch("trustpilot.cli.auth")
    def test_no_verbosity_with_post(self, auth_mock, client_mock):
        client_mock.post.return_value = self.response_mock

        result = self.runner.invoke(
            cli,
            _creds_list
            + [
                "-of",
                "raw",
                "post",
                "/v1/business-units/5400267300006400057a0113/reviews",
                "--data",
                '{"foo": "bar"}',
                "--content_type",
                "application/json",
            ],
        )
        print(result.output)
        assert result.output == self.expected_output

    @mock.patch("trustpilot.cli.client", autospec=True)
    @mock.patch("trustpilot.cli.auth")
    def test_no_verbosity_with_put(self, auth_mock, client_mock):
        client_mock.put.return_value = self.response_mock

        result = self.runner.invoke(
            cli,
            _creds_list
            + [
                "-of",
                "raw",
                "put",
                "/v1/business-units/5400267300006400057a0113/reviews",
                "--data",
                '{"foo": "bar"}',
                "--content_type",
                "application/json",
            ],
        )
        print(result.output)
        assert result.output == self.expected_output

    @mock.patch("trustpilot.cli.client", autospec=True)
    @mock.patch("trustpilot.cli.auth")
    def test_no_verbosity_with_delete(self, auth_mock, client_mock):
        client_mock.delete.return_value = self.response_mock

        result = self.runner.invoke(
            cli,
            _creds_list
            + [
                "-of",
                "raw",
                "delete",
                "/v1/business-units/5400267300006400057a0113/reviews",
            ],
        )

        print(result.output)
        assert result.output == self.expected_output
