"""
Settings for {{cookiecutter.package_name}} project.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

from {{cookiecutter.package_name}}.__version__ import __version__

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).parent.parent
LOG_DIR = Path.cwd() / "logs"
LOG_DIR.mkdir(exist_ok=True)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False") == "True"

# Application definition
ASGI_APPLICATION = "{{cookiecutter.package_name}}.asgi.application"

# Database settings
DATABASES = {
    "default": {
        "url": os.environ.get("DATABASE_DEFAULT"),
    }
}

# Internationalization
TIME_ZONE = "UTC"
USE_TZ = True

# OpenAPI settings
OPENAPI = {
    "title": "{{cookiecutter.package_name}} Title",
    "summary": "{{cookiecutter.package_name}} Summary.",
    "description": "{{cookiecutter.package_name}} as a base for new projects.",
    "version": __version__,
    "openapi_url": "/schema/" if DEBUG else None,
    "docs_url": "/schema/swagger/" if DEBUG else None,
    "redoc_url": "/schema/redoc/" if DEBUG else None,
    "license": {
        "name": "MIT",
    },
}


# Logging config
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "debug.log",
            "formatter": "verbose",
            "backupCount": 5,
            "maxBytes": 1024 * 1024 * 15,
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["file", "console"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
