from datetime import datetime
from decimal import Decimal
from typing import Annotated, Optional

from pydantic import ConfigDict, field_validator
from sqlmodel import Field, Relationship, SQLModel, Session
from sqlmodel import select

from dundie.utils.email import check_valid_email
from dundie.utils.user import generate_simple_password


class InvalidEmailError(ValueError): ...


class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    email: str = Field(
        nullable=False, index=True, sa_column_kwargs={"unique": True}
    )
    name: str = Field(nullable=False)
    dept: str = Field(nullable=False, index=True)
    role: str = Field(nullable=False)
    currency: str = Field(default="USD")

    balance: "Balance" = Relationship(back_populates="person")
    movement: "Movement" = Relationship(back_populates="person")
    user: "User" = Relationship(back_populates="person")

    def movements(self, session: Session):
        return session.exec(
            select(Movement)
            .where(Movement.person_id == self.id)
            .order_by(Movement.date.desc())
        ).all()

    def latest_movement(self, session: Session):
        """Query the Movement table for the latest movement for this person."""
        return session.exec(
            select(Movement)
            .where(Movement.person_id == self.id)
            .order_by(Movement.date.desc())
        ).first()

    @property
    def superuser(self):
        # TODO: campo, verificacao em uma tabela RBAC
        return self.email.split("@")[0] in ("schrute", "scott")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not check_valid_email(v):
            raise InvalidEmailError(f"Invalid email for {v!r}")
        return v

    def __str__(self) -> str:
        return f"{self.name} - {self.role}"


class Balance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    person_id: int = Field(
        foreign_key="person.id",
        sa_column_kwargs={"unique": True},
        # there is only one balance for each person
    )
    value: Annotated[Decimal, Field(decimal_places=3, default=0)]

    person: Person = Relationship(back_populates="balance")

    model_config = ConfigDict(json_encoders={Person: lambda p: p.id})


class Movement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    person_id: int = Field(foreign_key="person.id")
    actor: str = Field(nullable=False, index=True)
    value: Annotated[Decimal, Field(decimal_places=3, default=0)]
    date: datetime = Field(default_factory=lambda: datetime.now())

    person: Person = Relationship(back_populates="movement")

    model_config = ConfigDict(json_encoders={Person: lambda p: p.id})


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    person_id: int = Field(
        foreign_key="person.id", sa_column_kwargs={"unique": True}
    )
    password: str = Field(default_factory=generate_simple_password)

    person: Person = Relationship(back_populates="user")

    model_config = ConfigDict(json_encoders={Person: lambda p: p.id})
