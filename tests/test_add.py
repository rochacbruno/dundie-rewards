import pytest

from dundie.core import add, load, read
from dundie.database import add_person, commit, connect

from .constants import PEOPLE_FILE


@pytest.mark.unit
def test_add_movement():
    db = connect()

    pk = "joe@doe.com"
    data = {"role": "Salesman", "dept": "Sales", "name": "Joe Doe"}
    _, created = add_person(db, pk, data)
    assert created is True

    pk = "jim@doe.com"
    data = {"role": "Manager", "dept": "Management", "name": "Jim Doe"}
    _, created = add_person(db, pk, data)
    assert created is True

    commit(db)

    add(-30, email="joe@doe.com")
    add(90, dept="Management")

    db = connect()
    assert db["balance"]["joe@doe.com"] == 470
    assert db["balance"]["jim@doe.com"] == 190


@pytest.mark.unit
def test_add_balance_for_dept():
    load(PEOPLE_FILE)
    original = read(dept="Sales")

    add(100, dept="Sales")

    modified = read(dept="Sales")
    for index, person in enumerate(modified):
        assert person["balance"] == original[index]["balance"] + 100


@pytest.mark.unit
def test_add_balance_for_person():
    load(PEOPLE_FILE)
    original = read(email="jim@dundlermifflin.com")

    add(-30, email="jim@dundlermifflin.com")

    modified = read(email="jim@dundlermifflin.com")
    for index, person in enumerate(modified):
        assert person["balance"] == original[index]["balance"] - 30
