<<<<<<< HEAD
"""Core module of dundie"""
import os
from csv import reader
from typing import Any, Dict, List

=======
"""Core module of dundie."""

import getpass
import os
import sys
from csv import reader
from typing import Any, Dict, List

import pytest
>>>>>>> projeto-dundie-rewards/main
from sqlmodel import select

from dundie.database import get_session
from dundie.models import Person
from dundie.settings import DATEFMT
from dundie.utils.db import add_movement, add_person
from dundie.utils.exchange import get_rates
from dundie.utils.log import get_logger

log = get_logger()
Query = Dict[str, Any]
ResultDict = List[Dict[str, Any]]


def load(filepath: str) -> ResultDict:
<<<<<<< HEAD
    """Loads data from filepath to the database.
=======
    """Load data from filepath to the database.
>>>>>>> projeto-dundie-rewards/main

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
<<<<<<< HEAD
    """Read data from db and filters using query
=======
    """Read data from db and filters using query.
>>>>>>> projeto-dundie-rewards/main

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
<<<<<<< HEAD
        sql = sql.where(*query_statements)  # WHERE ...

    with get_session() as session:
        currencies = session.exec(
            select(Person.currency).distinct(Person.currency)
        )
        rates = get_rates(currencies)
        results = session.exec(sql)
        for person in results:
            total = rates[person.currency].value * person.balance[0].value
            return_data.append(
                {
                    "email": person.email,
                    "balance": person.balance[0].value,
                    "last_movement": person.movement[-1].date.strftime(
                        DATEFMT
                    ),
=======
        sql = sql.where(*query_statements)  # WHERE AuthenticationError()

    with get_session() as session:
        # obtemos toda as currencies existentes ["BRL", "USD", "EUR"]
        currencies = session.exec(
            select(Person.currency).distinct(Person.currency)
        )
        rates = get_rates(currencies)  # type: ignore

        results = session.exec(sql)
        for person in results:
            p1 = rates[person.currency].value
            p2 = person.balance[0].value  # type: ignore
            total = p1 * p2
            return_data.append(
                {
                    "email": person.email,
                    "balance": person.balance[0].value,  # type: ignore
                    "last_movement": person.movement[  # type: ignore
                        -1
                    ].date.strftime(
                        DATEFMT
                    ),  # type: ignore
>>>>>>> projeto-dundie-rewards/main
                    **person.dict(exclude={"id"}),
                    **{"value": total},
                }
            )
    return return_data


def add(value: int, **query: Query):
<<<<<<< HEAD
    """Add value to each record on query"""
=======
    """Add value to each record on query."""
>>>>>>> projeto-dundie-rewards/main
    query = {k: v for k, v in query.items() if v is not None}
    people = read(**query)

    if not people:
        raise RuntimeError("Not Found")

    with get_session() as session:
        user = os.getenv("USER")
        for person in people:
            instance = session.exec(
                select(Person).where(Person.email == person["email"])
            ).first()
<<<<<<< HEAD
            add_movement(session, instance, value, user)

        session.commit()
=======
            add_movement(session, instance, value, user)  # type: ignore

        session.commit()


@pytest.mark.skip(reason="no way of currently testing this")
def access_allowed():
    """Check user is correct."""
    count: int = 0
    id_email = access_email()
    _ = access_passwd(count, id_email)


def access_email():
    """..."""
    with get_session() as session:
        logig: str = input("LOGIN: ").strip()
        if logig != "" and logig is not None:
            id_user = session.execute(
                f"SELECT id FROM person WHERE email='{logig}'"
            )
            try:
                id = [row for row in id_user.first()]
                id = int("".join(map(str, id)))
            except TypeError:
                print("The user doesn't exist. Please digit valid email.")
                return access_email()
        else:
            print("Field empty deny permission, Please field fill.")
            return access_email()
        email = session.execute(f"SELECT email FROM person WHERE id='{id}'")
        email1 = [row for row in email.first()]
        email1 = "".join(map(str, email1))
        if logig == email1:
            return id
        else:
            print("You don't have access, please set your email")
            return access_email()


def access_passwd(count, id_acess):
    """..."""
    count += 1
    id_acess = id_acess
    if 6 < count:
        print("Exceeded put password attempt numbers.")
        sys.exit(1)

    elif count == 5:
        print("You only have more than one attempt put a password.")
        return access_passwd(count, id_acess)
    else:
        with get_session() as session:
            passwd = getpass.getpass("SENHA: ")
            if passwd != "" and passwd is not None:
                id_pass = session.execute(
                    f"SELECT person_id FROM user WHERE password='{passwd}'"
                )
                try:
                    person_id = [row for row in id_pass.first()]
                    person_id = int("".join(map(str, person_id)))
                    _pass = session.execute(
                        f"SELECT password FROM user "
                        f"WHERE person_id='{person_id}'"
                    )
                    pass_wd = [row for row in _pass.first()]
                    pass_wd = "".join(map(str, pass_wd))
                except TypeError:
                    print(
                        "If your password is wrong,"
                        " please digit the right password!"
                    )

                    return access_passwd(count, id_acess)
            else:
                print("Field password is empty, Please field fill.")
                return access_passwd(count, id_acess)

        if pass_wd == passwd and id_acess == person_id:
            print("acessando")
        else:
            print("You don't have access, please set your password")
            return access_passwd(count, id_acess)
>>>>>>> projeto-dundie-rewards/main
