<<<<<<< HEAD
"""Core module for dundie - (controler or base or paste load)."""
import os
from csv import reader

from dundie.database import add_movement, add_person, commit, connect
=======
"""Core module for dundie - (controler or base or paste load)"""
from csv import reader

from dundie.database import add_person, commit, connect
>>>>>>> 3675e88a678e05be48a17838b5c5f4eb528f7ce5
from dundie.utils.log import get_logger

log = get_logger()


def load(filepath):
<<<<<<< HEAD
    """Load data from filepath to the database.

=======
    """Loads data from filepath to the database.
>>>>>>> 3675e88a678e05be48a17838b5c5f4eb528f7ce5
    #python -m doctest -v dundie/core.py

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
        pk = person_data.pop("email")
        person, created = add_person(db, pk, person_data)

        return_data = person.copy()
        return_data["created"] = created
        return_data["email"] = pk
        people.append(return_data)

    commit(db)
    return people
<<<<<<< HEAD


def read(**query):
    """Read data from db and filters using query."""
    db = connect()
    return_data = []
    for pk, data in db["people"].items():
        dept = query.get("dept")
        if dept and dept != data["dept"]:

            continue
        # WALRUS / Assignment Expression - python 3.8
        if (email := query.get("email")) and email != pk:

            continue

        return_data.append(
            {
                "email": pk,
                "balance": db["balance"][pk],
                "last_movement": db["movement"][pk][-1]["date"],
                **data,
            }
        )
    return return_data


def add(value, **query):
    """Add value to each record on query."""
    people = read(**query)
    if not people:
        raise RuntimeError("Not Found")

    db = connect()
    user = os.getenv("USER")
    for person in people:
        add_movement(db, person["email"], value, user)
    commit(db)
=======
>>>>>>> 3675e88a678e05be48a17838b5c5f4eb528f7ce5
