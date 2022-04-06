import pytest

from dundie.database import (
    EMPTY_DB,
    ORM,
    add_movement,
    add_person,
    commit,
    connect,
)
from dundie.models import Balance, InvalidEmailError, Movement, Person


@pytest.mark.unit
def test_ensure_database_is_test():
    from dundie.database import DATABASE_PATH

    assert "test.json" in DATABASE_PATH


@pytest.mark.unit
def test_database_schema():
    db = connect()
    db_keys = {ORM.get_table_name(model) for model in db}
    assert db_keys == EMPTY_DB.keys()


@pytest.mark.unit
def test_commit_to_database():
    db = connect()
    pk = "joe@doe.com"
    data = {"name": "Joe Doe", "role": "Salesman", "dept": "Sales"}
    db[Person].append(Person(pk=pk, **data))
    commit(db)

    db = connect()
    assert db[Person].get_by_pk("joe@doe.com").dict() == {"pk": pk, **data}


@pytest.mark.unit
def test_add_person_for_the_first_time():
    pk = "joe@doe.com"
    data = {"role": "Salesman", "dept": "Sales", "name": "Joe Doe"}
    db = connect()
    _, created = add_person(db, Person(pk=pk, **data))
    assert created is True
    commit(db)

    db = connect()
    assert db[Person].get_by_pk(pk) == {"pk": pk, **data}
    assert db[Balance].get_by_pk(pk).value == 500
    assert len(db[Movement].filter(person__pk=pk)) > 0
    assert db[Movement].filter(person__pk=pk).first().value == 500


@pytest.mark.unit
def test_negative_add_person_invalid_email():
    with pytest.raises(InvalidEmailError):
        add_person({}, Person(pk=".@bla"))


@pytest.mark.unit
def test_add_or_remove_points_for_person():
    pk = "joe@doe.com"
    data = {"role": "Salesman", "dept": "Sales", "name": "Joe Doe"}
    db = connect()
    person = Person(pk=pk, **data)
    _, created = add_person(db, person)
    assert created is True
    commit(db)

    db = connect()
    before = db[Balance].get_by_pk(pk).value

    add_movement(db, person, -100, "manager")
    commit(db)

    db = connect()
    after = db[Balance].get_by_pk(pk).value

    assert after == before - 100
    assert after == 400
    assert before == 500
