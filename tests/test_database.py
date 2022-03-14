import pytest
from dundie.database import add_movement, add_person, commit, connect


@pytest.mark.unit
def test_ensure_database_is_test():
    from dundie.database import DATABASE_PATH
    assert "test.json" in DATABASE_PATH


@pytest.mark.unit
def test_database_save_first_time_person():
    db = connect()
    data = {
        "role": "Security Guard",
        "dept": "Security",
        "name": "Joe Doe",
    }
    pk = "joe@doe.com"

    person, created = add_person(db, pk, data)
    assert created is True
    commit(db)
    assert person["name"] == data["name"]

    person = db["people"][pk]
    assert person["name"] == "Joe Doe"

    balance = db["balance"][pk]
    assert balance == 500


@pytest.mark.unit
def test_add_balance_for_person():
    db = connect()
    pk = "joe@doe.com"
    data = {
        "role": "Security Guard",
        "dept": "Security",
        "name": "Joe Doe",
    }
    person, created = add_person(db, pk, data)
    assert created is True
    commit(db)
    assert person["name"] == data["name"]

    before = db["balance"][pk]
    add_movement(db, pk, -100, "me")
    commit(db)

    after = db["balance"][pk]

    assert before > after
    assert after == before - 100
