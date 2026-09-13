from sqlalchemy import Column, Integer, MetaData, Table
from sqlmodel import Field

from {{cookiecutter.package_name}}.db.models import Model


class Article(Model, table=True):  # type: ignore[call-arg]
    """Concrete model with a single-column primary key."""

    title: str = Field(index=True)
    summary: str | None = None


class Composite(Model):
    """Non-table model whose ``__table__`` is substituted for pk tests."""

    code: int


def test_pk_is_none_when_no_table():
    assert Model().pk is None


def test_pk_single_column():
    article = Article(id=42, title="Hello")
    assert article.pk == 42


def test_pk_composite_column():
    metadata = MetaData()
    table = Table(
        "composite",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("code", Integer, primary_key=True),
    )
    composite = Composite(id=1, code=7)
    composite.__table__ = table

    assert composite.pk == (1, 7)


def test_equality_uses_primary_key_only():
    first = Article(id=1, title="One")
    second = Article(id=1, title="Two")
    other = Article(id=2, title="Two")

    assert first == second
    assert first != other


def test_str_and_repr():
    article = Article(id=1, title="One")

    assert str(article) == "Article object (1)"
    assert repr(article) == "<Article: Article object (1)>"
