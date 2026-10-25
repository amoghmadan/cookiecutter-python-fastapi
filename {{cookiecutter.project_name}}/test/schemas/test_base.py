from types import SimpleNamespace

from {{cookiecutter.package_name}}.schemas.base import Schema


class Sample(Schema):
    first_name: str
    last_name: str


def test_schema_serializes_camel_case_for_the_ui():
    payload = Sample(first_name="Ada", last_name="Lovelace")

    assert payload.model_dump(by_alias=True) == {
        "firstName": "Ada",
        "lastName": "Lovelace",
    }


def test_schema_accepts_camel_case_input():
    payload = Sample.model_validate({"firstName": "Ada", "lastName": "Lovelace"})

    assert payload.first_name == "Ada"
    assert payload.last_name == "Lovelace"


def test_schema_accepts_snake_case_input():
    payload = Sample.model_validate({"first_name": "Ada", "last_name": "Lovelace"})

    assert payload.first_name == "Ada"
    assert payload.last_name == "Lovelace"


def test_schema_builds_from_attributes():
    entity = SimpleNamespace(first_name="Ada", last_name="Lovelace")

    payload = Sample.model_validate(entity)

    assert payload.first_name == "Ada"
    assert payload.last_name == "Lovelace"
