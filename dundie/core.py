"""Core module of dundie"""
import os
from csv import reader

from dundie.database import add_person, commit, connect, add_movement
from dundie.utils.log import get_logger

log = get_logger()


def load(filepath):
    """Loads data from filepath to the database.

    >>> len(load('assets/people.csv'))
    3
    """
    try:
        data = reader(open(filepath))
    except FileNotFoundError as e:
        log.error(str(e))
        raise e

    db = connect()
    people = []
    for line in data:
        person_data = dict(
            zip(
                ["name", "dept", "role", "email"],
                [item.strip() for item in line],
            )
        )
        pk = person_data.pop("email")
        person, created = add_person(db, pk, person_data)
        person["created"] = created
        person["email"] = pk
        people.append(person)

    commit(db)
    return people


def read(**query):
    """Returns a subset fo the database"""
    db = connect()
    return_data = []
    for pk, data in db["people"].items():
        if (dept := query.get("dept")) and dept != data["dept"]:
            continue
        if (email := query.get("email")) and email != data["email"]:
            continue
        return_data.append(
            {
                "name": data["name"],
                "dept": data["dept"],
                "role": data["role"],
                "email": pk,
                "balance": db["balance"][pk],
                "last_movement": db["movement"][pk][-1]["date"]
            }
        )
    return return_data


def add(value, **query):
    """adds value to each one on query"""
    return_data = read(**query)
    if not return_data:
        raise RuntimeError("Not found")

    db = connect()
    user = os.getenv("USER")
    for person in return_data:
        add_movement(db, person["email"], value, user)
    commit(db)
