import os

import pytest
from click.testing import CliRunner
from sqlmodel import select

from dundie.cli import main, show
from dundie.database import get_session
from dundie.models import Person, User
from dundie.utils.db import add_person

from .constants import DUNDIE_ADMIN_USER, DUNDIE_ADMIN_USER_PASSWORD

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.medium
def test_show_positive_call_show_command():
    """test command show"""

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

        out = cmd.invoke(show)

        assert out.exit_code == 0
        assert "joe" in out.output
        assert "jim" in out.output


@pytest.mark.integration
@pytest.mark.medium
def test_show_call_show_command_with_only_infor_user():
    """test command show"""

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
        joe_update.password = "qWert123"
        session.add(joe_update)
        session.commit()
        session.refresh(joe_update)

        os.environ["DUNDIE_USER"] = "joe@doe.com"
        os.environ["DUNDIE_PASSWORD"] = "qWert123"

        out = cmd.invoke(show)

        assert out.exit_code == 0
        assert "joe" in out.output
        assert "jim" not in out.output


@pytest.mark.integration
@pytest.mark.medium
def test_show_call_show_command_with_only_infor_user_manager():
    """test command show"""

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
        jim_update.password = "qWert123"
        session.add(jim_update)
        session.commit()
        session.refresh(jim_update)

        os.environ["DUNDIE_USER"] = "jim@doe.com"
        os.environ["DUNDIE_PASSWORD"] = "qWert123"

        out = cmd.invoke(show)

        assert out.exit_code == 0
        assert "joe" in out.output
        assert "jim" in out.output
        assert "otto" not in out.output


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize("wrong_command", ["mostrar", "showw", "ver"])
def test_show_negative_call_show_command_with_wrong_params(wrong_command):
    """test command show"""
    out = cmd.invoke(main, wrong_command)
    assert out.exit_code != 0
    assert f"No such command '{wrong_command}'." in out.output
