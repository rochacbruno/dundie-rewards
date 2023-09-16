import getpass
import os

from sqlmodel import select

from dundie.database import get_session
from dundie.models import InvalidEmailError, Person, User
from dundie.utils.email import check_valid_email


class InvalidPasswordError(Exception):
    ...


class UserNotFoundError(Exception):
    ...


class AuthenticationError(Exception):
    ...


def validation_user_if_exist(user: str) -> bool:
    """Validation User if exist in database"""

    if not check_valid_email(user):
        raise InvalidEmailError(f"Invalid email for {user!r}")

    with get_session() as session:

        instance = session.exec(
            select(Person.email).where(Person.email == user)
        ).first()

        if instance == user:
            return True
        if not instance:
            raise UserNotFoundError(f"User not found: {user!r}")


def validation_password(user: str, password: str) -> bool:
    """Ensure password is correct"""

    with get_session() as session:

        instance_person = session.exec(
            select(Person.id).where(Person.email == user)
        ).first()

        instance_user = session.exec(
            select(User.password).where(User.person_id == instance_person)
        ).first()

        if instance_user == password:
            return True
        else:
            raise InvalidPasswordError(f"Invalid password for {user!r}")


def require_password() -> bool:
    """Input user and password"""

    user = os.getenv("DUNDIE_USER")
    password = os.getenv("DUNDIE_PASSWORD")

    if user and password:
        if validation_user_if_exist(user):
            if validation_password(user, password):
                return True

    elif user and not password:
        if validation_user_if_exist(user):
            password = getpass.getpass()
            if validation_password(user, password):
                os.environ["DUNDIE_PASSWORD"] = password
                return True

    elif not user:
        user = input(str("User: "))
        if validation_user_if_exist(user):
            password = getpass.getpass()
            if validation_password(user, password):
                os.environ["DUNDIE_USER"] = user
                os.environ["DUNDIE_PASSWORD"] = password
                return True

    else:
        return False
