import pytest
from sqlmodel import select

from dundie.database import get_session
from dundie.models import Person, User
from dundie.utils.db import add_person
from dundie.utils.email import check_valid_email
from dundie.utils.login import (
    InvalidPasswordError,
    UserNotFoundError,
    validation_password,
    validation_user_if_exist,
)
from dundie.utils.user import password_encrypt


@pytest.mark.unit
@pytest.mark.parametrize(
    "address", ["bruno@rocha.com", "joe@doe.com", "a@b.pt"]
)
def test_positive_check_valid_email(address):
    """Ensure email is valid."""
    assert check_valid_email(address) is True


@pytest.mark.unit
@pytest.mark.parametrize("address", ["bruno@.com", "@doe.com", "a@b"])
def test_negative_check_valid_email(address):
    """Ensure email is invalid."""
    assert check_valid_email(address) is False


@pytest.mark.unit
@pytest.mark.parametrize("user", ["joe@doe.com", "jim@doe.com"])
def test_positive_validation_user_if_exist(user):
    """Ensure user is valid"""
    with get_session() as session:
        joe = {
            "email": "joe@doe.com",
            "name": "Joe Doe",
            "dept": "Sales",
            "role": "Salesman",
        }

        instance_joe = Person(**joe)
        _, created = add_person(session=session, instance=instance_joe)
        assert created is True

        jim = {
            "email": "jim@doe.com",
            "name": "Jim Doe",
            "dept": "Management",
            "role": "Manager",
        }

        instance_jim = Person(**jim)
        _, created = add_person(session=session, instance=instance_jim)
        assert created is True

        session.commit()

        assert validation_user_if_exist(user) is True


@pytest.mark.unit
@pytest.mark.parametrize("user", ["flavio@doe.com", "jose@doe.com"])
def test_negative_validation_user_if_exist(user):
    """Ensure user is valid"""
    with pytest.raises(UserNotFoundError):
        with get_session() as session:
            joe = {
                "email": "joe@doe.com",
                "name": "Joe Doe",
                "dept": "Sales",
                "role": "Salesman",
            }

            instance_joe = Person(**joe)
            _, created = add_person(session=session, instance=instance_joe)
            assert created is True

            jim = {
                "email": "jim@doe.com",
                "name": "Jim Doe",
                "dept": "Management",
                "role": "Manager",
            }

            instance_jim = Person(**jim)
            _, created = add_person(session=session, instance=instance_jim)
            assert created is True

            session.commit()

            validation_user_if_exist(user)


@pytest.mark.unit
@pytest.mark.parametrize(
    ["user", "password"],
    [
        ("joe@doe.com", password_encrypt("12345678")),
        ("jim@doe.com", password_encrypt("abcdefgh")),
    ],
)
def test_negative_validation_password(user, password):
    """Ensure password is valid"""
    with pytest.raises(InvalidPasswordError):
        with get_session() as session:
            joe = {
                "email": "joe@doe.com",
                "name": "Joe Doe",
                "dept": "Sales",
                "role": "Salesman",
            }

            instance_joe = Person(**joe)
            _, created = add_person(session=session, instance=instance_joe)
            assert created is True

            jim = {
                "email": "jim@doe.com",
                "name": "Jim Doe",
                "dept": "Management",
                "role": "Manager",
            }

            instance_jim = Person(**jim)
            _, created = add_person(session=session, instance=instance_jim)
            assert created is True

            session.commit()

            validation_password(user, password)


@pytest.mark.unit
@pytest.mark.parametrize(
    ["user", "password_"], [("joe@doe.com", password_encrypt("qWert123"))]
)
def test_positive_validation_password(user, password_):
    """Ensure password is valid"""
    with get_session() as session:
        joe = {
            "email": "joe@doe.com",
            "name": "Joe Doe",
            "dept": "Sales",
            "role": "Salesman",
        }

        instance_joe = Person(**joe)
        _, created = add_person(session=session, instance=instance_joe)

        assert created is True

        joe_update = session.exec(
            select(User).where(User.person == instance_joe)
        ).first()
        joe_update.password = password_encrypt("qWert123")
        session.add(joe_update)
        session.commit()
        session.refresh(joe_update)

        assert validation_password(user, password_) is True
