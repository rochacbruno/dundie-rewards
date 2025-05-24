import pytest

from dundie.core import add, load, read
from dundie.database import get_session
from dundie.models import Person
from dundie.utils.db import add_person

from .constants import PEOPLE_FILE


@pytest.fixture(scope="function", autouse=True)
def auth(monkeypatch):
    with get_session() as session, monkeypatch.context() as ctx:
        data = {
            "role": "Manager",
            "dept": "Management",
            "name": "Michael Scott",
            "email": "scott@dm.com",
        }
        password = "1234"
        person, _ = add_person(session, Person(**data), password)
        ctx.setenv("DUNDIE_EMAIL", person.email)
        ctx.setenv("DUNDIE_PASSWORD", password)
        session.commit()
        yield


@pytest.mark.unit
def test_add_movement():
    with get_session() as session:
        data = {
            "role": "Salesman",
            "dept": "Sales",
            "name": "Joe Doe",
            "email": "joe@doe.com",
        }
        joe, created = add_person(session, Person(**data))
        assert created is True

        data = {
            "role": "Manager",
            "dept": "Management",
            "name": "Jim Doe",
            "email": "jim@doe.com",
        }
        jim, created = add_person(session, Person(**data))
        assert created is True

        session.commit()

        add(-30, email="joe@doe.com")
        add(90, dept="Management")
        session.refresh(joe)
        session.refresh(jim)

        assert joe.balance.value == 470
        assert jim.balance.value == 190


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
