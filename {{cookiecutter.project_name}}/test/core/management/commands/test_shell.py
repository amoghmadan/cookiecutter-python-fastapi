import sys
import types

from {{cookiecutter.package_name}}.core.management.commands import shell as shell_module
from {{cookiecutter.package_name}}.core.management.commands.shell import cli, get_namespace


class FakeIPython(types.ModuleType):
    def __init__(self, calls: dict[str, object]) -> None:
        super().__init__("IPython")
        self.calls = calls

    def start_ipython(self, argv: list[str], user_ns: dict[str, object]) -> None:
        self.calls.update(argv=argv, ns=user_ns)


class FakeBpython(types.ModuleType):
    def __init__(self, calls: dict[str, object]) -> None:
        super().__init__("bpython")
        self.calls = calls

    def embed(self, namespace: dict[str, object]) -> None:
        self.calls.update(ns=namespace)


def test_get_namespace_without_imports():
    assert get_namespace(no_imports=True) == {}


def test_get_namespace_with_imports():
    namespace = get_namespace(no_imports=False)
    assert set(namespace) == {"os", "sys"}


def test_shell_runs_inline_command(cli_client):
    result = cli_client.invoke(cli, ["--command", "print('hello from shell')"])

    assert result.exit_code == 0
    assert "hello from shell" in result.output


def test_launch_python_executes_pythonstartup(monkeypatch, tmp_path):
    startup = tmp_path / "startup.py"
    startup.write_text("boot_value = 42\n")
    monkeypatch.setenv("PYTHONSTARTUP", str(startup))
    monkeypatch.setattr(
        shell_module.os.path, "expanduser", lambda _: str(tmp_path / "missing.py")
    )
    monkeypatch.setattr(shell_module.code, "interact", lambda **_: None)
    namespace: dict[str, object] = {}

    shell_module.launch_python(namespace, no_startup=False)

    assert namespace["boot_value"] == 42


def test_launch_python_reports_startup_errors(monkeypatch, tmp_path, capsys):
    broken = tmp_path / "broken.py"
    broken.write_text("def broken(:\n")
    monkeypatch.setenv("PYTHONSTARTUP", str(broken))
    monkeypatch.setattr(
        shell_module.os.path, "expanduser", lambda _: str(tmp_path / "missing.py")
    )
    monkeypatch.setattr(shell_module.code, "interact", lambda **_: None)

    shell_module.launch_python({}, no_startup=False)

    assert "Error loading startup file" in capsys.readouterr().err


def test_launch_python_survives_missing_readline(monkeypatch):
    monkeypatch.setitem(sys.modules, "readline", None)
    monkeypatch.setattr(shell_module.code, "interact", lambda **_: None)

    shell_module.launch_python({}, no_startup=True)


def test_launch_ipython_uses_namespace(monkeypatch):
    calls: dict[str, object] = {}
    monkeypatch.setitem(sys.modules, "IPython", FakeIPython(calls))
    namespace: dict[str, object] = {"answer": 42}

    shell_module.launch_ipython(namespace)

    assert calls == {"argv": [], "ns": namespace}


def test_launch_bpython_uses_namespace(monkeypatch):
    calls: dict[str, object] = {}
    monkeypatch.setitem(sys.modules, "bpython", FakeBpython(calls))
    namespace: dict[str, object] = {"answer": 42}

    shell_module.launch_bpython(namespace)

    assert calls == {"ns": namespace}


def test_shell_interface_ipython(cli_client, monkeypatch):
    calls: dict[str, object] = {}
    monkeypatch.setitem(sys.modules, "IPython", FakeIPython(calls))

    result = cli_client.invoke(cli, ["--interface", "ipython"])

    assert result.exit_code == 0
    assert calls["argv"] == []


def test_shell_interface_bpython(cli_client, monkeypatch):
    calls: dict[str, object] = {}
    monkeypatch.setitem(sys.modules, "bpython", FakeBpython(calls))

    result = cli_client.invoke(cli, ["--interface", "bpython"])

    assert result.exit_code == 0
    assert "ns" in calls


def test_shell_interface_python(cli_client, monkeypatch):
    monkeypatch.setattr(shell_module.code, "interact", lambda **_: None)

    result = cli_client.invoke(
        cli, ["--interface", "python", "--no-startup", "--no-imports"]
    )

    assert result.exit_code == 0


def test_shell_reports_missing_explicit_interface(cli_client, monkeypatch):
    monkeypatch.setitem(sys.modules, "IPython", None)

    result = cli_client.invoke(cli, ["--interface", "ipython"])

    assert result.exit_code == 1
    assert "Couldn't import 'ipython'" in result.stderr


def test_shell_without_interface_falls_back_to_python(cli_client, monkeypatch):
    monkeypatch.setitem(sys.modules, "IPython", None)
    monkeypatch.setitem(sys.modules, "bpython", None)
    monkeypatch.setattr(shell_module.code, "interact", lambda **_: None)

    result = cli_client.invoke(cli, ["--no-startup"])

    assert result.exit_code == 0
