from {{cookiecutter.package_name}}.schemas.response import PingResponse


def test_ping_response_schema():
    payload = PingResponse(reply="Pong")
    assert payload.reply == "Pong"
    assert payload.model_dump() == {"reply": "Pong"}
