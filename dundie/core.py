"""Core module of dundie"""
import os
from csv import reader
from typing import Any, Dict, List

from decouple import config
from sqlmodel import select

from dundie.database import get_session
from dundie.models import Person, User
from dundie.settings import DATEFMT, VAR_ENV
from dundie.utils.db import add_movement, add_person
from dundie.utils.exchange import get_rates
from dundie.utils.log import get_logger

log = get_logger()
Query = Dict[str, Any]
ResultDict = List[Dict[str, Any]]


class AuthenticationError(Exception):
    pass


def load(filepath: str) -> ResultDict:
    """Loads data from filepath to the database.

    >>> len(load('assets/people.csv'))
    2
    """
    try:
        csv_data = reader(open(filepath))
    except FileNotFoundError as e:
        log.error(str(e))
        raise e

    people = []
    headers = ["name", "dept", "role", "email", "currency"]

    with get_session() as session:
        for line in csv_data:
            person_data = dict(zip(headers, [item.strip() for item in line]))
            instance = Person(**person_data)
            person, created = add_person(session, instance)
            return_data = person.dict(exclude={"id"})
            return_data["created"] = created
            people.append(return_data)

        session.commit()

    return people


def read(**query: Query) -> ResultDict:
    """Read data from db and filters using query

    read(email="joe@doe.com")
    """
    query = {k: v for k, v in query.items() if v is not None}
    return_data = []

    query_statements = []
    if "dept" in query:
        query_statements.append(Person.dept == query["dept"])
    if "email" in query:
        query_statements.append(Person.email == query["email"])
    sql = select(Person)  # SELECT FROM PERSON
    if query_statements:
        sql = sql.where(*query_statements)  # WHERE ...

    with get_session() as session:
        currencies = session.exec(
            select(Person.currency).distinct(Person.currency)
        )
        rates = get_rates(list(currencies))
        results = session.exec(sql)
        for person in results:
            total = rates[person.currency].value * person.balance[0].value
            return_data.append(
                {
                    "email": person.email,
                    "balance": person.balance[0].value,  # type: ignore
                    "last_movement": person.movement[-1].date.strftime(
                        DATEFMT
                    ),
                    **person.dict(exclude={"id"}),
                    **{"value": total},
                }
            )
    return return_data


def add(value: int, **query: Query):
    """Add value to each record on query"""
    query = {k: v for k, v in query.items() if v is not None}
    people = read(**query)

    if not people:
        raise AuthenticationError("User not Found!")

    with get_session() as session:
        user = os.getenv("USER")
        for person in people:
            instance = session.exec(
                select(Person).where(Person.email == person["email"])
            ).first()
            add_movement(session, instance, value, user)

        session.commit()


def access_allowed():
    dundie_user = config("DUNDIE_USER")
    dundie_pw = config("DUNDIE_PASSWORD")

    if dundie_user and dundie_pw:
        return True
    return False


def login(email, password):
    with get_session() as session:
        person = session.exec(
            select(Person, User).where(
                Person.email == email and User.password == password
            )
        ).first()

        if not person:
            raise AuthenticationError(
                "You don't have access, please request your acess to the admin"
            )

        with open(VAR_ENV, "w") as f:
            f.write(f"DUNDIE_USER={person[0].email}\n")
            f.write(f"DUNDIE_PASSWORD={person[1].password}")

        return person
