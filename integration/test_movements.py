import os

import pytest
from click.testing import CliRunner
from sqlmodel import select

from dundie.cli import main, movements
from dundie.database import get_session
from dundie.models import Person, User
from dundie.utils.db import add_person
from dundie.utils.user import password_encrypt

from .constants import DUNDIE_ADMIN_USER, DUNDIE_ADMIN_USER_PASSWORD

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.medium
def test_movements_positive_call_movements_command():
    """test command movements"""

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

        os.environ["DUNDIE_USER"] = DUNDIE_ADMIN_USER
        os.environ["DUNDIE_PASSWORD"] = DUNDIE_ADMIN_USER_PASSWORD

        out = cmd.invoke(movements)

        assert out.exit_code == 0
        assert "Joe" in out.output
        assert "Jim" in out.output


@pytest.mark.integration
@pytest.mark.medium
def test_movements_call_movements_command_with_only_infor_user():
    """test command movements"""

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

        joe_update = session.exec(
            select(User).where(User.person == instance_joe)
        ).first()
        joe_update.password = password_encrypt("qWert123")
        session.add(joe_update)
        session.commit()
        session.refresh(joe_update)

        os.environ["DUNDIE_USER"] = "joe@doe.com"
        os.environ["DUNDIE_PASSWORD"] = password_encrypt("qWert123")

        out = cmd.invoke(movements)

        assert out.exit_code == 0
        assert "Joe" in out.output
        assert "Jim" not in out.output


@pytest.mark.integration
@pytest.mark.medium
def test_movements_call_movements_command_with_only_infor_user_manager():
    """test command movements"""

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

        otto = {
            "email": "otto@doe.com",
            "name": "Otto Doe",
            "dept": "TI",
            "role": "Software Enginer",
        }

        instance_otto = Person(**otto)
        _, created = add_person(session=session, instance=instance_otto)
        assert created is True

        jim = {
            "email": "jim@doe.com",
            "name": "Jim Doe",
            "dept": "Sales",
            "role": "Manager",
        }

        instance_jim = Person(**jim)
        _, created = add_person(session=session, instance=instance_jim)
        assert created is True

        jim_update = session.exec(
            select(User).where(User.person == instance_jim)
        ).first()
        jim_update.password = password_encrypt("qWert123")
        session.add(jim_update)
        session.commit()
        session.refresh(jim_update)

        os.environ["DUNDIE_USER"] = "jim@doe.com"
        os.environ["DUNDIE_PASSWORD"] = password_encrypt("qWert123")

        out = cmd.invoke(movements)

        assert out.exit_code == 0
        assert "Joe" in out.output
        assert "Jim" in out.output
        assert "Otto" not in out.output


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize("wrong_command", ["report", "moviments", "movimento"])
def test_movements_negative_call_movements_command_with_wrong_params(
    wrong_command,
):
    """test command movements"""
    out = cmd.invoke(main, wrong_command)
    assert out.exit_code != 0
    assert f"No such command '{wrong_command}'." in out.output


@pytest.mark.integration
def test_movements_call_movements_empty():
    """test command movements, call movements when empty"""

    os.environ["DUNDIE_USER"] = DUNDIE_ADMIN_USER
    os.environ["DUNDIE_PASSWORD"] = DUNDIE_ADMIN_USER_PASSWORD

    out = cmd.invoke(movements)

    assert out.exit_code == 0
    assert "Nothing to show" in out.output
