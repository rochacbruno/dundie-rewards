import json
from datetime import datetime

from dundie.settings import DATABASE_PATH
from dundie.utils.email import send_email, check_valid_email
from dundie.utils.user import generate_simple_password

EMPTY_DB = {"people": {}, "balance": {}, "movement": {}, "users": {}}
"""DB EXAMPLE
{
    "people": {
        "jim@dundlermifflin.com": {
            "name": "Jim Halpert",
            "dept": "Sales",
            "role": "Salesman",
            "created": false,
            "email": "jim@dundlermifflin.com"
        },
    },
    "balance": {
        "jim@dundlermifflin.com": 500,
    },
    "movement": {
        "jim@dundlermifflin.com": [
            {
                "date": "2022-03-15T12:01:01.362019",
                "actor": "system",
                "value": 500
            }
        ],
    },
    "users": {
        "jim@dundlermifflin.com": {
            "password": "mVCXtqIc"
        }
    }
}

"""


def connect():
    try:
        with open(DATABASE_PATH, "r") as database_file:
            return json.loads(database_file.read())
    except (json.JSONDecodeError, FileNotFoundError):
        return EMPTY_DB


def commit(db):
    with open(DATABASE_PATH, "w") as database_file:
        database_file.write(json.dumps(db, indent=4))


def add_movement(db, pk, value, actor="system"):
    movements = db["movement"].setdefault(pk, [])
    movements.append(
        {
            "date": datetime.now().isoformat(),
            "actor": actor,
            "value": value,
        }
    )
    db["balance"][pk] = sum([item["value"] for item in movements])


def set_initial_balance(db, pk, info):
    """Sets initial balance
    -  IF role == manager: starts with 100 points
    - If role != manager: starts with 500 points
    also add the movement tracker
    """
    value = 100 if info["role"] == "Manager" else 500
    add_movement(db, pk, value)


def set_initial_password(db, pk):
    password = generate_simple_password(8)
    db["users"].setdefault(pk, {})
    db["users"][pk]["password"] = password
    return password


def add_person(db, pk, data):
    """Save person data to database.json:people table.

    For each item in data:
    - Email is the unique primary key
    - If exists update, if not create
    - Sets the initial balance
    """
    if not check_valid_email(pk):
        raise ValueError(f"{pk} is not a valid e-mail")
    table = db["people"]
    person = table.get(pk, {})
    created = not bool(person)
    person.update(data)
    table[pk] = person
    if created:
        set_initial_balance(db, pk, person)
        password = set_initial_password(db, pk)
        send_email("me@me.com", pk, "passwd", password)
    return person, created
