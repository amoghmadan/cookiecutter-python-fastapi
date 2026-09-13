import importlib
import os
from types import ModuleType
from typing import Any

from pydantic import ConfigDict, create_model
from pydantic._internal._model_construction import ModelMetaclass

from {{cookiecutter.package_name}}.conf import global_settings

ENVIRONMENT_VARIABLE = "FASTAPI_SETTINGS_MODULE"


def settings_from_module(module: str) -> ModelMetaclass:
    """
    Generate settings class with default values to start the project.
    :param module: str, reference to module
    :return: ModelMetaclass
    """
    fields: dict[str, tuple[Any, Any]] = {}
    for attr in dir(global_settings):
        if attr.isupper():
            value: Any = getattr(global_settings, attr)
            fields[attr] = (type(value), value)

    mod: ModuleType = importlib.import_module(module)
    for attr in dir(mod):
        if attr.isupper():
            value = getattr(mod, attr)
            fields[attr] = (type(value), value)
        if attr.islower() and attr.startswith("celery_"):  # Extra
            value = getattr(mod, attr)
            fields[attr.lower()] = (type(value), value)

    return create_model(  # ty: ignore[no-matching-overload]
        "Settings",
        __config__=ConfigDict(arbitrary_types_allowed=True),
        **fields,
    )


settings_module: str | None = os.environ.get(ENVIRONMENT_VARIABLE)
if not settings_module:
    raise ValueError(f"{ENVIRONMENT_VARIABLE} not set.")

Settings: ModelMetaclass = settings_from_module(settings_module)
settings: Settings = Settings()  # ty: ignore[invalid-type-form]

__all__ = ["settings"]
