import importlib
import json
from collections import UserList, defaultdict
from typing import TYPE_CHECKING, Any, Dict, Optional

if TYPE_CHECKING:
    from pydantic import BaseModel

from dundie.settings import DATABASE_PATH, EMAIL_FROM
from dundie.utils.email import send_email

EMPTY_DB: Dict[str, Dict[str, Any]] = {
    "people": {},
    "balance": {},
    "movement": {},
    "users": {},
}


DB = Dict["BaseModel", "ResultList"]


class NotFoundError(Exception):
    ...


class ResultList(UserList):
    def first(self) -> Any:
        return self[0]

    def last(self) -> Any:
        return self[-1]

    def get_by_pk(self, pk: str) -> Any:
        if len(self) == 0:
            raise NotFoundError(f"{pk} not found")
        try:
            if hasattr(self[0], "pk"):
                return ResultList(
                    item for item in self if item.pk == pk
                ).first()
            return ResultList(
                item for item in self if item.person.pk == pk
            ).first()
        except KeyError:
            raise NotFoundError(f"{pk} not found")

    def filter(self, **query: Dict[str, Any]) -> "ResultList":
        if not query:
            return self
        return_data = ResultList()
        for item in self:
            add_item = []
            for q, v in query.items():
                if "__" in q:
                    sub_model, sub_field = q.split("__")
                    related = getattr(item, sub_model)
                    if getattr(related, sub_field) == v:
                        add_item.append(True)
                else:
                    if getattr(item, q) == v:
                        add_item.append(True)
                    else:
                        add_item.append(False)
            if add_item and all(add_item):
                return_data.append(item)
        return return_data


class ORM:
    """Mapeamento entre "table" no JSON e classes em models"""

    MAPPING: Dict[str, str] = {
        "people": "dundie.models.Person",
        "balance": "dundie.models.Balance",
        "movement": "dundie.models.Movement",
        "users": "dundie.models.User",
    }

    @classmethod
    def get_model_class(cls, table_name: str) -> Any:
        module, obj = cls.MAPPING[table_name].rsplit(".", 1)
        return getattr(importlib.import_module(module), obj)

    @classmethod
    def get_table_name(cls, model: Any) -> str:
        inverted_orm = {v.split(".")[-1]: k for k, v in cls.MAPPING.items()}
        return inverted_orm[model.__name__]

    @classmethod
    def serialize(cls, db) -> Dict[str, Any]:
        """Turns Model instances back to json compatible dict."""
        raw_db: Dict[str, Any] = defaultdict(dict)
        for model, instances in db.items():
            table_name = cls.get_table_name(model)
            raw_db[table_name]  # initialize default dict
            for instance in instances:
                raw_instance = json.loads(instance.json())
                if table_name == "people":
                    raw_db[table_name][raw_instance.pop("pk")] = raw_instance
                elif table_name == "balance":
                    raw_db[table_name][instance.person.pk] = raw_instance[
                        "value"
                    ]
                elif table_name == "movement":
                    table = raw_db[table_name]
                    table.setdefault(instance.person.pk, [])
                    raw_instance.pop("person")
                    table[instance.person.pk].append(raw_instance)
                else:
                    raw_instance.pop("person")
                    raw_db[table_name][instance.person.pk] = raw_instance
        return raw_db

    @classmethod
    def deserialize(cls, raw_data: Dict[str, Any]) -> Dict[Any, ResultList]:
        """Turns JSON in to model isntances"""
        results: Dict[Any, ResultList] = defaultdict(ResultList)
        indexes = {}
        for table_name, data in raw_data.items():
            Model = cls.get_model_class(table_name)
            results[Model]  # initialize default dict
            if table_name == "people":
                for pk, person_data in data.items():
                    instance = Model(pk=pk, **person_data)
                    indexes[pk] = instance
                    results[Model].append(instance)
            elif table_name == "balance":
                for pk, balance_data in data.items():
                    instance = Model(person=indexes[pk], value=balance_data)
                    results[Model].append(instance)
            elif table_name == "users":
                for pk, user_data in data.items():
                    instance = Model(person=indexes[pk], **user_data)
                    results[Model].append(instance)
            elif table_name == "movement":
                for pk, movements in data.items():
                    for movement in movements:
                        instance = Model(person=indexes[pk], **movement)
                        results[Model].append(instance)
        return results


def connect() -> Dict[Any, ResultList]:
    """Connects to the database, returns dict data"""
    try:
        with open(DATABASE_PATH, "r") as database_file:
            raw_data = json.loads(database_file.read())
    except (json.JSONDecodeError, FileNotFoundError):
        raw_data = EMPTY_DB

    # transform raw data from json to model objects / Deserialize
    results = ORM.deserialize(raw_data)
    return results


def commit(db: DB):
    """Save db back to the database file."""
    # transform model objects back to json database / Serialize
    raw_db = ORM.serialize(db)

    if raw_db.keys() != EMPTY_DB.keys():
        raise RuntimeError(f"Database Schema is invalid. {raw_db.keys()}")

    final_data = json.dumps(raw_db, indent=4)
    with open(DATABASE_PATH, "w") as database_file:
        database_file.write(final_data)


def add_person(db: DB, instance: Any):
    """Saves person data to database.

    - If exists, update, else create
    - Set initial balance (managers = 100, others = 500)
    - Generate a password if user is new and send_email
    """
    Person = ORM.get_model_class("people")
    table = db[Person]
    existing = table.filter(pk=instance.pk)
    created = len(existing) == 0
    if created:
        table.append(instance)
        set_initial_balance(db, instance)
        password = set_initial_password(db, instance)
        send_email(EMAIL_FROM, instance.pk, "Your dundie password", password)
    else:
        existing_data = existing.first().dict()
        new_data = instance.dict()
        existing_data.update(new_data)
        table.remove(existing)
        table.append(Person(**existing_data))
    return instance, created


def set_initial_password(db: DB, instance: Any) -> str:
    """Generated and saves password"""
    User = ORM.get_model_class("users")
    user = User(person=instance)  # password generated by model
    db[User].append(user)
    return user.password


def set_initial_balance(db: DB, person: Any):
    """Add movement and set initial balance"""
    value = 100 if person.role == "Manager" else 500
    add_movement(db, person, value)


def add_movement(
    db: DB, person: Any, value: int, actor: Optional[str] = "system"
):
    """Adds movement to user account.

    Example::

        add_movement(db, Person(...), 100, "me")

    """
    Movement = ORM.get_model_class("movement")
    db[Movement].append(Movement(person=person, value=value, actor=actor))
    movements = [item for item in db[Movement] if item.person.pk == person.pk]

    Balance = ORM.get_model_class("balance")

    # reset balance table for the user
    db[Balance] = ResultList(
        [item for item in db[Balance] if item.person.pk != person.pk]
    )

    db[Balance].append(
        Balance(person=person, value=sum([item.value for item in movements]))
    )
