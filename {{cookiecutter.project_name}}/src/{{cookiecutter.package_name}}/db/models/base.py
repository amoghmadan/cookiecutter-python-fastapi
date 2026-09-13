from sqlmodel import BigInteger, Column, Field, SQLModel


class Model(SQLModel):
    """Base: Model"""

    __abstract__ = True
    __table__ = None

    id: int | None = Field(
        default=None,
        sa_column=Column(
            BigInteger(), primary_key=True, autoincrement=True, nullable=False
        ),
    )

    @property
    def pk(self) -> None | int | str | tuple:
        if self.__table__ is None:
            return None
        pk_columns = [c.name for c in self.__table__.primary_key.columns]
        if len(pk_columns) == 1:
            return getattr(self, pk_columns[0], None)
        return tuple(getattr(self, col, None) for col in pk_columns)

    def __eq__(self, other) -> bool:
        return self.pk == other.pk

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self}>"

    def __str__(self) -> str:
        return f"{self.__class__.__name__} object ({self.pk})"
