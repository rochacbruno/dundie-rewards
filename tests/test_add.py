<<<<<<< HEAD
=======
"""Test add user in database."""
>>>>>>> projeto-dundie-rewards/main
import pytest

from dundie.core import add, load, read
from dundie.database import get_session
from dundie.models import Person
from dundie.utils.db import add_person

from .constants import PEOPLE_FILE


@pytest.mark.unit
def test_add_movement():
<<<<<<< HEAD
=======
    """Test add movement of the two users."""
>>>>>>> projeto-dundie-rewards/main
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
<<<<<<< HEAD

=======
>>>>>>> projeto-dundie-rewards/main
        add(-30, email="joe@doe.com")
        add(90, dept="Management")
        session.refresh(joe)
        session.refresh(jim)

        assert joe.balance[0].value == 470
        assert jim.balance[0].value == 190


@pytest.mark.unit
def test_add_balance_for_dept():
<<<<<<< HEAD
=======
    """access_allowed()"""
>>>>>>> projeto-dundie-rewards/main
    load(PEOPLE_FILE)
    original = read(dept="Sales")

    add(100, dept="Sales")

    modified = read(dept="Sales")
    for index, person in enumerate(modified):
        assert person["balance"] == original[index]["balance"] + 100


@pytest.mark.unit
def test_add_balance_for_person():
<<<<<<< HEAD
    load(PEOPLE_FILE)
    original = read(email="jim@dundlermifflin.com")

    add(-30, email="jim@dundlermifflin.com")

    modified = read(email="jim@dundlermifflin.com")
    for index, person in enumerate(modified):
        assert person["balance"] == original[index]["balance"] - 30
=======
    """access_allowed()"""
    load(PEOPLE_FILE)
    original = read(email="jim@dundiemifflin.com")

    add(-30, email="jim@dundiemifflin.com")

    modified = read(email="jim@dundiemifflin.com")
    for index, person in enumerate(modified):
        assert person["balance"] == int(original[index]["balance"]) - 30
>>>>>>> projeto-dundie-rewards/main
