import click
import json
import logging
import sys
import os.path as path
from inspect import getsourcefile


current_dir = path.dirname(path.abspath(getsourcefile(lambda: 0)))
sys.path.insert(0, current_dir[: current_dir.rfind(path.sep)])
logger = logging.getLogger(__name__)

from trustpilot import client, auth, VERSION
from collections import OrderedDict


@click.pass_context
def get_verbosity(ctx):
    return ctx.meta.get("trustpilot.verbosity", 0)


@click.pass_context
def get_output_format(ctx):
    output_format = ctx.meta.get("trustpilot.outputformat", "json") or "json"
    return output_format


def format_response(response):
    content = response.text

    output_format = get_output_format()

    if output_format == "raw":
        lines = []
        lines.extend(["url", response.url, "\n"])
        lines.extend(["status", str(response.status_code), "\n"])
        if get_verbosity():
            lines.extend(
                [
                    e
                    for t in [
                        (f"headers.{key}", str(value), "\n")
                        for key, value in response.headers.items()
                    ]
                    for e in t
                ]
            )
        lines.extend(["content", content])
        return "\n".join(lines)
    elif output_format == "json":
        try:
            content = response.json()
        except ValueError:
            pass
        output = OrderedDict()
        output["url"] = response.url
        output["status"] = response.status_code
        if get_verbosity():
            headers = response.headers
            output["headers"] = OrderedDict((k, headers[k]) for k in headers)
        output["content"] = content
        return json.dumps(output, indent=2)


@click.group(invoke_without_command=True)
@click.pass_context
@click.option("--host", type=str, help="Host name", envvar="TRUSTPILOT_API_HOST")
@click.option(
    "--version", type=str, help="Api version", envvar="TRUSTPILOT_API_VERSION"
)
@click.option("--key", type=str, help="Api key", envvar="TRUSTPILOT_API_KEY")
@click.option("--secret", type=str, help="Api secret", envvar="TRUSTPILOT_API_SECRET")
@click.option(
    "--token_issuer_host",
    type=str,
    default="",
    help="Token issuer host name",
    envvar="TRUSTPILOT_API_TOKEN_ISSUER_HOST",
)
@click.option(
    "--username",
    type=str,
    default="",
    help="Trustpilot username",
    envvar="TRUSTPILOT_USERNAME",
)
@click.option(
    "--password",
    type=str,
    default="",
    help="Trustpilot password",
    envvar="TRUSTPILOT_PASSWORD",
)
@click.option("--config", "-c", type=click.File("r"), help="Json config file name")
@click.option("--env", "-e", type=click.File("r"), help="Dot env file")
@click.option(
    "--outputformat",
    "-of",
    type=click.Choice(["json", "raw"], case_sensitive=False),
    default="json",
    help="Output format, default=json",
)
@click.option("-v", "--verbose", count=True, help="Verbosity level")
def cli(ctx, **kwargs):
    splash = r"""
         _____              _         _ _       _
        |_   _|            | |       (_) |     | |
          | |_ __ _   _ ___| |_ _ __  _| | ___ | |_
          | | '__| | | / __| __| '_ \| | |/ _ \| __|
          | | |  | |_| \__ \ |_| |_) | | | (_) | |_
          \_/_|   \__,_|___/\__| .__/|_|_|\___/ \__|
                               | |
                               |_|
          ___        _   _____ _ _            _
         / _ \      (_) /  __ \ (_)          | |
        / /_\ \_ __  _  | /  \/ |_  ___ _ __ | |_
        |  _  | '_ \| | | |   | | |/ _ \ '_ \| __|
        | | | | |_) | | | \__/\ | |  __/ | | | |_
        \_| |_/ .__/|_|  \____/_|_|\___|_| |_|\__|
              | |
              |_|   """
    splash = click.style(splash, fg="green") + "\n"

    values_dict = {}
    config_file = kwargs.pop("config")

    if config_file:
        values_dict.update(json.load(config_file))

    env_file = kwargs.pop("env")
    if env_file:
        env_file_lines = env_file.read().split("\n")
        values_dict.update(
            dict(
                (key, value[0])
                for key, *value in (line.split("=", 1) for line in env_file_lines)
                if key
            )
        )

    # setup verbosity level for global access
    verbosity = kwargs.get("verbose")
    ctx.meta["trustpilot.verbosity"] = verbosity

    # setup output format
    output_format = kwargs.get("outputformat")
    ctx.meta["trustpilot.outputformat"] = output_format

    # setup logging (increasing information levels)
    # _ : content, url, status_code
    # v : headers
    # vv: logging.INFO level
    # vvv: logging.DEBUG level
    levels = {2: logging.INFO, 3: logging.DEBUG}
    logging_level = levels.get(verbosity, logging.CRITICAL)

    logger.setLevel(logging_level)
    if logging_level > logging.DEBUG:
        # disable urllib3 logging
        client.disable_ssl_warnings()

    if ctx.invoked_subcommand is None:
        click.echo("\n".join([splash, ctx.get_help()]))
        return

    # create default session
    try:
        client.default_session.setup(
            api_host=kwargs.pop("host")
            or values_dict.get("TRUSTPILOT_API_HOST")
            or "https://api.tp-staging.com",
            api_version=kwargs.pop("version")
            or values_dict.get("TRUSTPILOT_API_VERSION")
            or "v1",
            api_key=kwargs.pop("key") or values_dict["TRUSTPILOT_API_KEY"],
            api_secret=(
                kwargs.pop("secret") or values_dict.get("TRUSTPILOT_API_SECRET", None)
            ),
            token_issuer_host=(
                kwargs.pop("token_issuer_host")
                or values_dict.get("TRUSTPILOT_API_TOKEN_ISSUER_HOST", None)
            ),
            username=kwargs.pop("username")
            or values_dict.get("TRUSTPILOT_USERNAME", None),
            password=kwargs.pop("password")
            or values_dict.get("TRUSTPILOT_PASSWORD", None),
        )
    except KeyError as key:
        raise SystemExit("Missing argument: {}".format(key))


cli_command = cli.command(
    context_settings=dict(ignore_unknown_options=True, allow_extra_args=True)
)


@cli_command
def create_access_token():
    """
    Get an access token
    """
    client.default_session.get_request_auth_headers()
    click.echo(client.default_session.access_token)


@cli_command
@click.argument("path")
def get(path):
    """
    Send a GET request
    """
    response = client.get(url=path)
    click.echo(format_response(response))


@cli_command
@click.argument("path")
@click.option("--data", type=str, help="json_data to post")
@click.option(
    "--content-type",
    type=str,
    default="application/json",
    help="content-type, default=application/json",
)
def post(path, data, content_type):
    """
    Send a POST request with specified data
    """
    headers = {"content-type": content_type}
    response = client.post(url=path, data=data, headers=headers)
    click.echo(format_response(response))


@cli_command
@click.argument("path")
def delete(path):
    """
    Send a DELETE request
    """
    response = client.delete(url=path)
    click.echo(format_response(response))


@cli_command
@click.argument("path")
@click.option("--data", type=str, help="json_data to post")
@click.option(
    "--content-type",
    type=str,
    default="application/json",
    help="content-type, default=application/json",
)
def put(path, data, content_type):
    """
    Send a PUT request with specified data
    """
    headers = {"content-type": content_type}
    response = client.put(url=path, data=data, headers=headers)
    click.echo(format_response(response))


@cli_command
@click.argument("path")
@click.option("--data", type=str, help="json_data to post")
@click.option(
    "--content-type",
    type=str,
    default="application/json",
    help="content-type, default=application/json",
)
def patch(path, data, content_type):
    """
    Send a PATCH request with specified data
    """
    headers = {"content-type": content_type}
    response = client.patch(url=path, data=data, headers=headers)
    click.echo(format_response(response))


if __name__ == "__main__":
    cli()
