import pytest

from dundie.core import load, read
from dundie.database import get_session
from dundie.models import Person
from dundie.utils.db import add_person

from .constants import PEOPLE_FILE


@pytest.mark.unit
def test_read_with_query():
    session = get_session()

    data = {
        "role": "Salesman",
        "dept": "Sales",
        "name": "Joe Doe",
        "email": "joe@doe.com",
    }
    _, created = add_person(session, Person(**data))
    assert created is True

    data = {
        "role": "Manager",
        "dept": "Management",
        "name": "Jim Doe",
        "email": "jim@doe.com",
    }
    _, created = add_person(session, Person(**data))
    assert created is True

    session.commit()

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
