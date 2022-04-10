from datetime import datetime
from typing import Optional

from pydantic import condecimal, validator
from sqlmodel import Field, Relationship, SQLModel

from dundie.utils.email import check_valid_email
from dundie.utils.user import generate_simple_password


class InvalidEmailError(Exception):
    ...


class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    name: str
    dept: str
    role: str

    balance: "Balance" = Relationship(back_populates="person")
    movement: "Movement" = Relationship(back_populates="person")
    user: "User" = Relationship(back_populates="person")

    @validator("email")
    def validate_email(cls, v: str) -> str:
        if not check_valid_email(v):
            raise InvalidEmailError(f"Invalid email for {v!r}")
        return v

    def __str__(self) -> str:
        return f"{self.name} - {self.role}"


class Balance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: int = Field(foreign_key="person.id")
    value: condecimal(decimal_places=3) = Field(default=0)

    person: Person = Relationship(back_populates="balance")

    class Config:
        json_encoders = {Person: lambda p: p.pk}


class Movement(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: int = Field(foreign_key="person.id")
    actor: str = Field(index=True)
    value: condecimal(decimal_places=3) = Field(default=0)
    date: datetime = Field(default_factory=lambda: datetime.now())

    person: Person = Relationship(back_populates="movement")

    class Config:
        json_encoders = {Person: lambda p: p.pk}


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    person_id: int = Field(foreign_key="person.id")
    password: str = Field(default_factory=generate_simple_password)

    person: Person = Relationship(back_populates="user")

    class Config:
        json_encoders = {Person: lambda p: p.pk}


# if __name__ == "__main__":
#     p = Person(pk="bruno@g.com", name="Bruno", dept="Sales", role="NA")
#     print(p)
#     print(p.json())

#     b = Balance(person=p, value=100)
#     print(b.json(models_as_dict=False))

#     m = Movement(person=p, date=datetime.now(), actor="sys", value=10)
#     print(m.json(models_as_dict=False))

#     u = User(person=p)
#     print(u.json(models_as_dict=False))

#     email = "invalid@"
#     try:
#         Person(pk=email)
#     except InvalidEmailError as e:
#         assert str(e) == f"Invalid email for {email!r}"
