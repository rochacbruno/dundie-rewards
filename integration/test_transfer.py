import os

import pytest
from click.testing import CliRunner
from sqlmodel import select

from dundie.cli import main, transfer
from dundie.database import get_session
from dundie.models import Person, User
from dundie.utils.db import add_person
from dundie.utils.login import UserNotFoundError

cmd = CliRunner()


@pytest.mark.integration
def test_transfer_positive():
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

        assert instance_joe.balance[0].value == 500

        out = cmd.invoke(transfer, args=("100", "jim@doe.com"))

        session.commit()
        session.refresh(instance_joe)

        assert instance_joe.balance[0].value == 400
        assert out.exit_code == 0
        assert "400" in out.output


@pytest.mark.integration
@pytest.mark.parametrize("wrong_command", ["transferir", "transferr", "move"])
def test_transfer_negative_call_transfer_command_with_wrong_params(
    wrong_command,
):
    """test command transfer"""
    out = cmd.invoke(main, wrong_command)
    assert out.exit_code != 0
    assert f"No such command '{wrong_command}'." in out.output


@pytest.mark.integration
def test_transfer_negative_with_argument_wrong():
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

        cmd.invoke(transfer, args=("100", "pam@doe.com"))

        assert UserNotFoundError


@pytest.mark.integration
def test_transfer_negative_with_enough_balance():
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

        jim_update = session.exec(
            select(User).where(User.person == instance_jim)
        ).first()
        jim_update.password = "qWert123"
        session.add(jim_update)
        session.commit()
        session.refresh(jim_update)

        os.environ["DUNDIE_USER"] = "jim@doe.com"
        os.environ["DUNDIE_PASSWORD"] = "qWert123"

        out = cmd.invoke(transfer, args=("200", "joe@doe.com"))

        session.commit()
        session.refresh(jim_update)

        assert instance_jim.balance[0].value == 100
        assert out.exit_code == 0
        assert "Falied!" in out.output
