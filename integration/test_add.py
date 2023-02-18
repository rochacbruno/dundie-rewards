import os

import pytest
from click.testing import CliRunner
from sqlmodel import select

from dundie.cli import add, main
from dundie.database import get_session
from dundie.models import Person, User
from dundie.utils.db import add_person
from dundie.utils.login import AccessDeniedError

from .constants import DUNDIE_ADMIN_USER, DUNDIE_ADMIN_USER_PASSWORD

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.medium
def test_add_positive_call_add_command():
    """test command add"""

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

        out = cmd.invoke(add, "100")

        assert out.exit_code == 0
        assert instance_joe.balance[0].value == 600
        assert instance_jim.balance[0].value == 200


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize("wrong_command", ["insert", "adicionar", "addd"])
def test_add_negative_call_add_command_with_wrong_params(wrong_command):
    """test command add"""
    out = cmd.invoke(main, wrong_command, "100")
    assert out.exit_code != 0
    assert f"No such command '{wrong_command}'." in out.output


@pytest.mark.unit
def test_add_negative_admin_interaction(request):
    """Test function add function."""

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
        joe_update.password = "qWert123"
        session.add(joe_update)
        session.commit()
        session.refresh(joe_update)

        os.environ["DUNDIE_USER"] = "joe@doe.com"
        os.environ["DUNDIE_PASSWORD"] = "qWert123"

        out = cmd.invoke(add, "100")

        assert out.exit_code != 0
        assert AccessDeniedError
