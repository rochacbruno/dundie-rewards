import os

import pytest
from click.testing import CliRunner
from sqlmodel import select

from dundie.database import get_session
from dundie.models import InvalidEmailError, Person, User
from dundie.utils.db import add_person
from dundie.utils.login import (
    AccessDeniedError,
    InvalidPasswordError,
    UserNotFoundError,
    require_password,
    validation_password,
    validation_user_if_exist,
)
from dundie.utils.user import password_encrypt
from integration.constants import (
    DUNDIE_ADMIN_USER,
    DUNDIE_ADMIN_USER_PASSWORD,
    DUNDIE_PASSWORD,
    DUNDIE_USER,
)

cmd = CliRunner()


@pytest.mark.unit
@pytest.mark.parametrize("user", ["joe@doe.com", "jim@doe.com"])
def test_positive_validation_user_if_exist(user):
    """Ensure user is valid and exist in db"""
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
    """Test user no exist in db"""
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
@pytest.mark.parametrize("user", ["flavio#doe.com"])
def test_negative_validation_user_if_exist_email_invalid(user):
    """Test user email invalid"""
    with pytest.raises(InvalidEmailError):
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


@pytest.mark.unit
@pytest.mark.parametrize(
    ["user", "password_"], [(DUNDIE_ADMIN_USER, password_encrypt("123456"))]
)
def test_positive_validation_password_invalid_password_admin(user, password_):
    """Test validation password with negative password admin"""
    with pytest.raises(InvalidPasswordError):
        validation_password(user, password_)


@pytest.mark.unit
def test_require_password_positive_mode_admin_only_true():
    """Test function with mode admin_only true"""

    os.environ["DUNDIE_USER"] = DUNDIE_ADMIN_USER
    os.environ["DUNDIE_PASSWORD"] = DUNDIE_ADMIN_USER_PASSWORD

    result = require_password(admin_only=True)

    assert result is True


@pytest.mark.unit
def test_require_password_negative_mode_admin_only_true():
    """Test negative function with mode admin_only true"""
    with pytest.raises(AccessDeniedError):
        os.environ["DUNDIE_USER"] = DUNDIE_USER
        os.environ["DUNDIE_PASSWORD"] = DUNDIE_PASSWORD

        require_password(admin_only=True)
