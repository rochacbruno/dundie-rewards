import pytest

from dundie.database import get_session
from dundie.models import InvalidEmailError, Person
from dundie.utils.db import add_movement, add_person


@pytest.mark.unit
def test_commit_to_database():
    with get_session() as session:
        data = {
            "email": "joe@doe.com",
            "name": "Joe Doe",
            "dept": "Sales",
            "role": "Salesman",
        }

        instance = Person(**data)
        add_person(session, instance)

        session.commit()

        return_data = {
            "email": instance.email,
            "name": instance.name,
            "dept": instance.dept,
            "role": instance.role,
        }

        assert return_data == data


@pytest.mark.unit
def test_add_person_for_the_first_time():
    with get_session() as session:
        data = {
            "email": "joe@doe.com",
            "name": "Joe Doe",
            "dept": "Sales",
            "role": "Salesman",
        }

        instance = Person(**data)

        _, created = add_person(session, instance)
        assert created is True

        session.commit()

        return_data = {
            "email": instance.email,
            "name": instance.name,
            "dept": instance.dept,
            "role": instance.role,
        }

        assert return_data == data
        assert instance.balance[0].value == 500
        assert instance.movement[0].value == 500
        assert len(instance.movement) > 0


@pytest.mark.unit
def test_negative_add_person_invalid_email():
    with pytest.raises(InvalidEmailError):
        with get_session() as _:
            data = {
                "email": "joe@",
                "name": "Joe Doe",
                "dept": "Sales",
                "role": "Salesman",
            }

            Person(**data)


@pytest.mark.unit
def test_add_or_remove_points_for_person():
    with get_session() as session:
        data = {
            "email": "joe@doe.com",
            "name": "Joe Doe",
            "dept": "Sales",
            "role": "Salesman",
        }

        instance = Person(**data)

        _, created = add_person(session, instance)
        assert created is True

        session.commit()

        before = instance.balance[0].value
        add_movement(session, instance, -100, "manager")

        session.commit()

        after = instance.balance[0].value

        assert after == before - 100
        assert before == 500
        assert after == 400


@pytest.mark.unit
def test_add_person_existing_person():
    with get_session() as session:
        data = {
            "email": "joe@doe.com",
            "name": "Joe Doe",
            "dept": "Sales",
            "role": "Salesman",
        }

        instance = Person(**data)

        _, created = add_person(session, instance)
        assert created is True

        session.commit()

        _, new_created = add_person(session, instance)

        assert new_created is False
