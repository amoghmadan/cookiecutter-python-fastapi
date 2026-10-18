import json
from types import SimpleNamespace
from typing import Self

from sqlalchemy.exc import IntegrityError

from {{cookiecutter.package_name}} import models as models_module
from {{cookiecutter.package_name}}.core.management.commands import loaddata as loaddata_module


class Widget:
    def __init__(self, id: int | None = None, **fields: object) -> None:
        self.id = id
        self.fields = fields


class RecordingSession:
    def __init__(self, fail_commit: bool = False) -> None:
        self.fail_commit = fail_commit
        self.added: list[Widget] = []
        self.committed = False
        self.rolled_back = False

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return None

    def add(self, obj: Widget) -> None:
        self.added.append(obj)

    async def commit(self) -> None:
        if self.fail_commit:
            raise IntegrityError("INSERT", {}, Exception("duplicate"))
        self.committed = True

    async def rollback(self) -> None:
        self.rolled_back = True


def setup_fixture(tmp_path, monkeypatch, fail_commit: bool = False) -> RecordingSession:
    (tmp_path / "src").mkdir()
    fixtures = tmp_path / "fixtures"
    fixtures.mkdir()
    (fixtures / "widgets.json").write_text(
        json.dumps(
            [
                {
                    "model": "{{cookiecutter.package_name}}.Widget",
                    "pk": 7,
                    "fields": {"name": "w"},
                }
            ]
        )
    )
    monkeypatch.setattr(
        loaddata_module, "settings", SimpleNamespace(BASE_DIR=tmp_path / "src")
    )
    created = RecordingSession(fail_commit=fail_commit)
    monkeypatch.setattr(loaddata_module, "session", lambda: created)
    monkeypatch.setattr(models_module, "Widget", Widget, raising=False)
    return created


def test_loaddata_creates_models(cli_client, tmp_path, monkeypatch):
    created = setup_fixture(tmp_path, monkeypatch)

    result = cli_client.invoke(loaddata_module.cli, ["--files", "widgets.json"])

    assert result.exit_code == 0
    assert created.committed
    assert len(created.added) == 1
    obj = created.added[0]
    assert obj.id == 7
    assert obj.fields == {"name": "w"}


def test_loaddata_rolls_back_on_integrity_error(cli_client, tmp_path, monkeypatch):
    created = setup_fixture(tmp_path, monkeypatch, fail_commit=True)

    result = cli_client.invoke(loaddata_module.cli, ["--files", "widgets.json"])

    assert result.exit_code == 0
    assert created.rolled_back
