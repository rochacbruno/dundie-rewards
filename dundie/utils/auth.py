import os
from functools import wraps

from sqlalchemy.orm import selectinload
from sqlmodel import select

from dundie.database import get_session
from dundie.models import Person


class AuthError(Exception):
    ...


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
                raise AuthError("User desn't exist")

            # TODO: in future we are going to encrypt.
            if person.user[0].password != password:
                raise AuthError("Authentication Error")

        # dependency injection
        return f(*args, from_person=person, **kwargs)

    return decorator
