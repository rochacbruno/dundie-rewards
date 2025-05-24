import os
from functools import wraps

from sqlalchemy.orm import selectinload
from sqlmodel import select

from dundie.database import get_session
from dundie.models import Person
from dundie.utils.user import verify_password


class AuthError(Exception): ...


def requires_auth(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        email = os.getenv("DUNDIE_EMAIL")
        password = os.getenv("DUNDIE_PASSWORD")
        if not all([email, password]):
            raise AuthError(
                "Variables DUNDIE_EMAIL and DUNDIE_PASSWORD not defined"
            )

        with get_session() as session:
            person = session.exec(
                select(Person)
                .options(
                    selectinload(Person.balance),
                    selectinload(Person.user),
                    selectinload(Person.movement),
                )
                .where(Person.email == email)
            ).first()

            if not person:
                raise AuthError("User doesn't exist")

            if not verify_password(password, person.user.password):
                raise AuthError("Authentication failed")

        # dependency injection
        return f(*args, from_person=person, **kwargs)

    return decorator
