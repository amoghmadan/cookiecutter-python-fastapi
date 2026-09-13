"""
ASGI config for {{cookiecutter.package_name}} project.

It exposes the ASGI callable as a module-level variable named ``application``.
"""

import os

from {{cookiecutter.package_name}}.core.asgi import get_asgi_application

os.environ.setdefault("FASTAPI_SETTINGS_MODULE", "{{cookiecutter.package_name}}.settings")

application = get_asgi_application()
