from {{cookiecutter.package_name}}.urls import urlpatterns
from {{cookiecutter.package_name}}.urls.api import api


def test_root_urls_include_api():
    assert urlpatterns == [api]
