import pytest
from sqlmodel import select

from dundie.database import get_session
from dundie.models import Person, User
from dundie.utils.db import add_person
from dundie.utils.user import generate_simple_password, password_decrypt


@pytest.mark.unit
def test_password_encrypt():
    """Ensure password encrypto pass"""
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

        new_password = generate_simple_password()

        joe_update = session.exec(
            select(User).where(User.person == instance_joe)
        ).first()
        joe_update.password = new_password
        session.add(joe_update)
        session.commit()
        session.refresh(joe_update)

        assert len(joe_update.password) == 100


@pytest.mark.unit
@pytest.mark.medium
def test_generate_simple_password():
    """Test generation of random simple password.
    TODO: Generate hashed complex passwords, encrypit it
    """
    passwords = []
    for _ in range(100):
        passwords.append(generate_simple_password(8))

    assert len(set(passwords)) == 100


@pytest.mark.unit
def test_password_decrypt():
    """Ensure password decrypto pass"""
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

        new_password = generate_simple_password()

        joe_update = session.exec(
            select(User).where(User.person == instance_joe)
        ).first()
        joe_update.password = new_password
        session.add(joe_update)
        session.commit()
        session.refresh(joe_update)

        assert len(password_decrypt(joe_update.password)) == 8
