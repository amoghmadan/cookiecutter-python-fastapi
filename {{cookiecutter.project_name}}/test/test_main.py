import os
import sys
import types
from unittest.mock import MagicMock

import pytest

from {{cookiecutter.package_name}} import __main__ as main_module
from {{cookiecutter.package_name}}.core import management


def test_main_sets_settings_module_and_runs_cli(monkeypatch):
    stub = MagicMock()
    monkeypatch.setattr(management, "execute_from_command_line", stub)
    monkeypatch.delenv("FASTAPI_SETTINGS_MODULE", raising=False)

    main_module.main()

    stub.assert_called_once()
    assert os.environ["FASTAPI_SETTINGS_MODULE"] == "{{cookiecutter.package_name}}.settings"


def test_main_raises_helpful_error_when_cli_is_unimportable(monkeypatch):
    fake = types.ModuleType("{{cookiecutter.package_name}}.core.management")
    monkeypatch.setitem(sys.modules, "{{cookiecutter.package_name}}.core.management", fake)

    with pytest.raises(ImportError, match="Couldn't import {{cookiecutter.package_name}}"):
        main_module.main()
