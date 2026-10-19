from {{cookiecutter.package_name}}.schemas.request import PingRequest


def test_ping_request_defaults_to_no_throw():
    payload = PingRequest()
    assert payload.throw is False
    assert payload.model_dump() == {"throw": False}


def test_ping_request_throw_flag():
    payload = PingRequest(throw=True)
    assert payload.throw is True
    assert payload.model_dump() == {"throw": True}
