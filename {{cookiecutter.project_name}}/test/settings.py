from {{cookiecutter.package_name}}.settings import *

DATABASES: dict[str, dict[str, str]] = {
    "default": {
        "url": "sqlite+aiosqlite:///:memory:",
    }
}
