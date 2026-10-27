from sqlalchemy import MetaData

from {{cookiecutter.package_name}}.conf import settings
from {{cookiecutter.package_name}}.db import DEFAULT_DB_ALIAS, metadata, metadatas


def test_metadatas_has_entry_per_configured_alias():
    assert set(metadatas) == set(settings.DATABASES)


def test_metadatas_are_distinct_metadata_instances():
    values = list(metadatas.values())

    assert all(isinstance(value, MetaData) for value in values)
    assert len({id(value) for value in values}) == len(values)


def test_default_metadata_is_the_configured_default_alias():
    assert metadata is metadatas[DEFAULT_DB_ALIAS]
