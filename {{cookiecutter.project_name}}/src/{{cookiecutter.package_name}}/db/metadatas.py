from sqlalchemy import MetaData

from {{cookiecutter.package_name}}.conf import settings

metadatas: dict[str, MetaData] = {alias: MetaData() for alias in settings.DATABASES}
