from typing import cast
from unittest.mock import MagicMock

from fastapi.params import Depends

from {{cookiecutter.package_name}}.dependencies import DBSes
from {{cookiecutter.package_name}}.dependencies.database import get_db


def test_get_db_returns_request_state_db():
    request = MagicMock()
    database = object()
    request.state.db = database

    assert get_db(request) is database


def test_dbses_is_a_depends_wrapping_get_db():
    assert cast(Depends, DBSes).dependency is get_db
