import uvicorn

from {{cookiecutter.package_name}}.__version__ import __version__
from {{cookiecutter.package_name}}.conf import settings
from {{cookiecutter.package_name}}.core import management
from {{cookiecutter.package_name}}.core.management import execute_from_command_line


def test_cli_version_option(cli_client):
    result = cli_client.invoke(execute_from_command_line, ["--version"])

    assert result.exit_code == 0
    assert result.output == f"{{cookiecutter.package_name}}, {__version__}\n"


def test_cli_verbose_option_is_accepted(cli_client):
    result = cli_client.invoke(execute_from_command_line, ["-v"])

    assert result.exit_code == 0


def test_cli_rejects_unknown_command(cli_client):
    result = cli_client.invoke(execute_from_command_line, ["unknown-command"])

    assert result.exit_code == 2


def test_cli_version_without_package_context(cli_client, monkeypatch):
    monkeypatch.setattr(management, "__package__", None)

    result = cli_client.invoke(execute_from_command_line, ["--version"])

    assert result.exit_code == 0
    assert result.output == ""


def test_runserver_starts_uvicorn(cli_client, monkeypatch):
    calls: dict[str, object] = {}
    monkeypatch.setattr(
        uvicorn,
        "run",
        lambda app, host=None, port=None, reload=None: calls.update(
            app=app, host=host, port=port, reload=reload
        ),
    )

    result = cli_client.invoke(
        execute_from_command_line, ["runserver", "--host", "0.0.0.0", "--port", "9000"]
    )

    assert result.exit_code == 0
    assert calls == {
        "app": "{{cookiecutter.package_name}}.asgi:application",
        "host": "0.0.0.0",
        "port": 9000,
        "reload": settings.DEBUG,
    }
