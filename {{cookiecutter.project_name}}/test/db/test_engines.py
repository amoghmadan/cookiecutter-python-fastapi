from {{cookiecutter.package_name}}.db import DEFAULT_DB_ALIAS, engine, engines, session, sessions


def test_engines_contains_default_alias():
    assert DEFAULT_DB_ALIAS in engines
    assert engines[DEFAULT_DB_ALIAS] is engine


def test_sessions_contains_default_alias():
    assert DEFAULT_DB_ALIAS in sessions
    assert sessions[DEFAULT_DB_ALIAS] is session
