"""
Default settings. Override these with settings in the module pointed to by the
FASTAPI_SETTINGS_MODULE environment variable.
"""

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ""  # nosec: B105

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Application definition
ASGI_APPLICATION = ""

# Database settings
DATABASES: dict[str, dict[str, str]] = {}

# Internationalization
TIME_ZONE = "UTC"
USE_TZ = True

# OpenAPI settings
OPENAPI = {
    "title": "App",
    "summary": "App Summary",
    "description": "App Description",
    "version": "0.1.0",
    "openapi_url": "/schema/",
    "docs_url": "/schema/swagger/",
    "redoc_url": "/schema/redoc/",
    "license": {
        "name": "Other/Proprietary License",
    },
}
