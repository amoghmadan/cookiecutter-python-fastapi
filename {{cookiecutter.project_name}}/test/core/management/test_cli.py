from {{cookiecutter.package_name}}.__version__ import __version__
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
