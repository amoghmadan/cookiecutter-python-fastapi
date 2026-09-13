from {{cookiecutter.package_name}}.core.management.commands.shell import cli, get_namespace


def test_get_namespace_without_imports():
    assert get_namespace(no_imports=True) == {}


def test_get_namespace_with_imports():
    namespace = get_namespace(no_imports=False)
    assert set(namespace) == {"os", "sys"}


def test_shell_runs_inline_command(cli_client):
    result = cli_client.invoke(cli, ["--command", "print('hello from shell')"])

    assert result.exit_code == 0
    assert "hello from shell" in result.output
