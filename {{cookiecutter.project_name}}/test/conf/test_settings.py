import importlib.util

import pytest

from {{cookiecutter.package_name}} import conf as conf_module
from {{cookiecutter.package_name}}.conf import settings, settings_from_module


def test_settings_uses_test_database():
    assert settings.DATABASES["default"]["url"] == "sqlite+aiosqlite:///:memory:"


def test_settings_include_global_defaults():
    assert isinstance(settings.DEBUG, bool)
    assert settings.TIME_ZONE == "UTC"
    assert settings.USE_TZ is True
    assert settings.SECRET_KEY is not None


def test_settings_from_module_merges_defaults_and_overrides():
    Settings = settings_from_module("test.fake_settings")
    resolved = Settings()

    assert resolved.CUSTOM_TEXT == "from-test-module"
    assert resolved.DEBUG is False
    assert resolved.USE_TZ is True


def test_settings_from_module_normalizes_celery_attributes():
    Settings = settings_from_module("test.fake_settings")
    resolved = Settings()

    assert resolved.celery_broker_url == "redis://localhost:6379/0"
    assert resolved.celery_task_default_queue == "{{cookiecutter.package_name}}"


def test_conf_raises_when_settings_module_is_unset(monkeypatch):
    monkeypatch.delenv("FASTAPI_SETTINGS_MODULE", raising=False)
    assert conf_module.__file__ is not None
    spec = importlib.util.spec_from_file_location(
        "conf_without_env", conf_module.__file__
    )
    assert spec is not None and spec.loader is not None
    fresh_module = importlib.util.module_from_spec(spec)

    with pytest.raises(ValueError, match="FASTAPI_SETTINGS_MODULE not set"):
        spec.loader.exec_module(fresh_module)
