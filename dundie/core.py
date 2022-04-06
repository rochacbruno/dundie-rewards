"""Core module of dundie"""
import os
from csv import reader
from typing import Any, Dict, List

from dundie.database import add_movement, add_person, commit, connect
from dundie.models import Balance, Movement, Person
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

    db = connect()
    people = []
    headers = ["name", "dept", "role", "email"]
    for line in csv_data:
        person_data = dict(zip(headers, [item.strip() for item in line]))
        instance = Person(pk=person_data.pop("email"), **person_data)
        person, created = add_person(db, instance)
        return_data = person.dict(exclude={"pk"})
        return_data["created"] = created
        return_data["email"] = person.pk
        people.append(return_data)

    commit(db)
    return people


def read(**query: Query) -> ResultDict:
    """Read data from db and filters using query

    read(email="joe@doe.com")
    """
    query = {k: v for k, v in query.items() if v is not None}
    db = connect()
    return_data = []
    if "email" in query:
        query["pk"] = query.pop("email")

    for person in db[Person].filter(**query):
        return_data.append(
            {
                "email": person.pk,
                "balance": db[Balance].get_by_pk(person.pk).value,
                "last_movement": db[Movement]
                .filter(person__pk=person.pk)[-1]
                .date,
                **person.dict(exclude={"pk"}),
            }
        )
    return return_data


def add(value: int, **query: Query):
    """Add value to each record on query"""
    query = {k: v for k, v in query.items() if v is not None}
    people = read(**query)

    if not people:
        raise RuntimeError("Not Found")

    db = connect()
    user = os.getenv("USER")
    for person in people:
        instance = db[Person].get_by_pk(person["email"])
        add_movement(db, instance, value, user)
    commit(db)
