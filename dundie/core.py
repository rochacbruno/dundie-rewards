"""Core module of dundie"""

from csv import reader
from typing import Any, Dict, List

from sqlmodel import select

from dundie.database import get_session
from dundie.models import Movement, Person
from dundie.settings import DATEFMT
from dundie.utils.auth import requires_auth
from dundie.utils.db import add_movement, add_person
from dundie.utils.exchange import get_rates
from dundie.utils.log import get_logger

log = get_logger()
Query = Dict[str, Any]
ResultDict = List[Dict[str, Any]]


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


def read(add_rates: bool = True, **query: Query) -> ResultDict:
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
        rates = get_rates(currencies) if add_rates else None
        results = session.exec(sql)
        for person in results:
            total = (
                rates[person.currency].value * person.balance.value
                if rates
                else person.balance.value
            )
            return_data.append(
                {
                    "email": person.email,
                    "balance": person.balance.value,
                    # "last_movement": person.movement.date.strftime(
                    #     DATEFMT
                    # ),
                    "last_movement": person.latest_movement(
                        session
                    ).date.strftime(DATEFMT),
                    **person.model_dump(exclude={"id"}),
                    **{"value": total},
                }
            )
    return return_data


@requires_auth
def add(value: int, from_person: Person, **query: Query):
    """Add value to each record on query"""
    query = {k: v for k, v in query.items() if v is not None}
    people = read(**query)

    if not people:  # pragma: no cover
        raise RuntimeError("Not Found")

    total = len(people) * value
    if from_person.balance.value < total and not from_person.superuser:
        raise RuntimeError(f"Not enough balance to transfer {total}")

    with get_session() as session:
        for person in people:
            instance = session.exec(
                select(Person).where(Person.email == person["email"])
            ).first()
            add_movement(session, instance, value, from_person.email)

            if not from_person.superuser:
                from_instance = session.exec(
                    select(Person).where(Person.email == from_person.email)
                ).first()
                # TODO: Here be the dragons!! BUG
                add_movement(
                    session,
                    from_instance,
                    -abs(value),
                    person["email"],
                )

        session.commit()


def get_transactions(email: str) -> ResultDict:
    """Get all transactions for a user by email

    Returns a list of movement records for the specified user
    """
    with get_session() as session:
        person = session.exec(
            select(Person).where(Person.email == email)
        ).first()

        if not person:
            return []

        movements = session.exec(
            select(Movement)
            .where(Movement.person_id == person.id)
            .order_by(Movement.date.desc())
        ).all()

        return [
            {
                "date": movement.date.strftime(DATEFMT),
                "actor": movement.actor,
                "value": float(movement.value),
                "email": person.email,
                "name": person.name,
                "dept": person.dept,
                "role": person.role,
            }
            for movement in movements
        ]
