from {{cookiecutter.package_name}}.api import api
from {{cookiecutter.package_name}}.urls import urlpatterns


def test_root_urls_include_api():
    assert urlpatterns == [api]
