"""Beging database with json."""
import json
from datetime import datetime

from dundie.settings import DATABASE_PATH, EMAIL_FROM
from dundie.utils.email import check_valid_email, send_email
from dundie.utils.user import generate_simple_password

EMPTY_DB: dict = {"people": {}, "balance": {}, "movement": {}, "user": {}}


def connect() -> dict:
    """Connect to the database, return dict data."""
    try:
        with open(DATABASE_PATH, "r") as database_file:
            return json.loads(database_file.read())
    except (json.JSONDecodeError, FileNotFoundError):
        return EMPTY_DB


def commit(db):
    """Save db back to the database file."""
    if db.keys() != EMPTY_DB.keys():
        raise RuntimeError("Database Schema is invalid")
    with open(DATABASE_PATH, "w") as database_file:
        database_file.write(json.dumps(db, indent=4))


def add_person(db, pk, data):
    """Save person data to database."""
    """
    - Email is unique (resolved by dictionary hash table)
    - If exists, update, else create
    - Set initial balance (managers = 100, others = 500)

    - Generate a password if user is new and send_email.



    """
    if not check_valid_email(pk):
        raise ValueError(f"{pk} is not a valid email")

    table = db["people"]
    person = table.get(pk, {})
    created = not bool(person)
    person.update(data)
    table[pk] = person
    if created:
        set_initial_balance(db, pk, person)
        password = set_initial_password(db, pk)
        send_email(EMAIL_FROM, pk, "your dundie password", password)
        # TODO: Encrypt and send only link not password

    return person, created


def set_initial_password(db, pk):
    """Generate and saves password."""
    db["user"].setdefault(pk, {})
    db["user"][pk]["password"] = generate_simple_password(8)
    return db["user"][pk]["password"]


def set_initial_balance(db, pk, person):
    """Add movement and set initial balance."""
    value = 100 if person["role"] == "Manager" else 500
    add_movement(db, pk, value)


def add_movement(db, pk, value, actor="system"):
    """Add movements to users acount."""
    """
    Example::

        add_movement(db, 'me@me.com', 100, 'me')
    """
    movements = db["movement"].setdefault(pk, [])
    movements.append(
        {
            "date": datetime.now().isoformat(),
            "actor": actor,
            "value": value,
        }
    )
    db["balance"][pk] = sum(item["value"] for item in movements)
