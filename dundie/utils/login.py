import getpass
import os
from typing import Any, Dict, List

from sqlmodel import select

from dundie.database import get_session
from dundie.models import InvalidEmailError, Person, User
from dundie.settings import DUNDIE_ADMIN_USER, DUNDIE_ADMIN_USER_PASSWORD
from dundie.utils.email import check_valid_email

Query = Dict[str, Any]
ResultDict = List[Dict[str, Any]]


class InvalidPasswordError(Exception):
    ...


class UserNotFoundError(Exception):
    ...


class AuthenticationError(Exception):
    ...


class AccessDeniedError(Exception):
    ...


def validation_user_if_exist(user: str) -> bool:
    """Validation User if exist in database"""

    if not check_valid_email(user):
        raise InvalidEmailError(f"Invalid email for {user!r}")

    elif user == DUNDIE_ADMIN_USER:
        return True

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

    if user == DUNDIE_ADMIN_USER:
        if password == DUNDIE_ADMIN_USER_PASSWORD:
            return True
        else:
            raise InvalidPasswordError(f"Invalid password for {user!r}")

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


def require_password(admin_only: bool) -> bool:
    """Input user and password"""

    user = os.getenv("DUNDIE_USER")
    password = os.getenv("DUNDIE_PASSWORD")

    if not admin_only:
        if user and password:
            if validation_user_if_exist(user):
                if validation_password(user, password):
                    return True

        if user and not password:
            if validation_user_if_exist(user):
                password = getpass.getpass()
                if validation_password(user, password):
                    os.environ["DUNDIE_PASSWORD"] = password
                    return True

        if not user:
            user = input(str("User: "))
            if validation_user_if_exist(user):
                password = getpass.getpass()
                if validation_password(user, password):
                    os.environ["DUNDIE_USER"] = user
                    os.environ["DUNDIE_PASSWORD"] = password
                    return True
        else:
            raise AccessDeniedError("⚠️ Access Denied ⚠️")

    elif admin_only:
        if user and password:
            if user == DUNDIE_ADMIN_USER:
                if password == DUNDIE_ADMIN_USER_PASSWORD:
                    return True

        if user and not password:
            if user == DUNDIE_ADMIN_USER:
                password = getpass.getpass()
                if password == DUNDIE_ADMIN_USER_PASSWORD:
                    os.environ["DUNDIE_PASSWORD"] = password
                    return True

        if not user:
            user = input(str("User: "))
            if user == DUNDIE_ADMIN_USER:
                password = getpass.getpass()
                if password == DUNDIE_ADMIN_USER_PASSWORD:
                    os.environ["DUNDIE_USER"] = user
                    os.environ["DUNDIE_PASSWORD"] = password
                    return True
        else:
            raise AccessDeniedError("⚠️ Access Denied ⚠️")


def handles_query_for_user(function: Any, **query: Query) -> ResultDict:
    """Manipulates read data from db and filters using query

    read(email="joe@doe.com")
    """
    query = {k: v for k, v in query.items() if v is not None}

    user = os.getenv("DUNDIE_USER")

    with get_session() as session:
        role = session.exec(
            select(Person.role).where(Person.email == user)
        ).first()
        dept = session.exec(
            select(Person.dept).where(Person.email == user)
        ).first()

    if user == DUNDIE_ADMIN_USER:
        return function(**query)
    else:
        if role == "Manager":
            return function(dept=dept)
        else:
            return function(email=user)
