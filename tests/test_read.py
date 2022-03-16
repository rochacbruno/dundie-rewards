import pytest

from dundie.core import load, read
from dundie.database import add_person, commit, connect

from .constants import PEOPLE_FILE


@pytest.mark.unit
def test_read_with_query():
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

    response = read()
    assert len(response) == 2

    response = read(dept="Management")
    assert len(response) == 1
    assert response[0]["name"] == "Jim Doe"

    response = read(email="joe@doe.com")
    assert len(response) == 1
    assert response[0]["name"] == "Joe Doe"


@pytest.mark.unit
def test_read_all_data():
    load(PEOPLE_FILE)
    result = read()
    assert len(result) == 3


@pytest.mark.unit
def test_read_only_one_dept():
    load(PEOPLE_FILE)
    result = read(dept="Sales")
    assert len(result) == 2


@pytest.mark.unit
def test_read_only_one_person():
    load(PEOPLE_FILE)
    result = read(email="jim@dundlermifflin.com")
    assert len(result) == 1
