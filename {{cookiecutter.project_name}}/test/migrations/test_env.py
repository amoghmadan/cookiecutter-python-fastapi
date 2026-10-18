import sqlite3

from alembic import command
from alembic.config import Config
from sqlmodel import MetaData

from {{cookiecutter.package_name}}.db.models.base import Model


def make_config(tmp_path) -> Config:
    ini = tmp_path / "alembic.ini"
    ini.write_text("[alembic]\nscript_location = {{cookiecutter.package_name}}:migrations\n")
    return Config(str(ini))


def test_env_runs_offline(tmp_path):
    command.upgrade(make_config(tmp_path), "head", sql=True)


def test_env_runs_online(tmp_path):
    command.upgrade(make_config(tmp_path), "head")


def test_env_autogenerate_skips_celery_tables(tmp_path, monkeypatch):
    database = tmp_path / "compare.sqlite3"
    connection = sqlite3.connect(database)
    connection.execute("CREATE TABLE celery_task (id INTEGER PRIMARY KEY)")
    connection.close()

    from {{cookiecutter.package_name}}.conf import settings

    monkeypatch.setattr(Model, "metadata", MetaData())
    monkeypatch.setitem(
        settings.DATABASES["default"], "url", f"sqlite+aiosqlite:///{database}"
    )

    command.check(make_config(tmp_path))
