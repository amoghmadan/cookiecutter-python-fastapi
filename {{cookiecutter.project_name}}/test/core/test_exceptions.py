import pytest

from {{cookiecutter.package_name}}.core.exceptions import Error


def test_error_is_exception_with_message():
    error = Error("boom")

    assert isinstance(error, Exception)
    assert str(error) == "boom"


def test_error_can_be_raised_and_caught():
    with pytest.raises(Error, match="boom"):
        raise Error("boom")
