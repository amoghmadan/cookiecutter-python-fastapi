from {{cookiecutter.package_name}}.schemas.response import Pong


def test_pong_schema():
    payload = Pong(reply="Pong")
    assert payload.reply == "Pong"
    assert payload.model_dump() == {"reply": "Pong"}
