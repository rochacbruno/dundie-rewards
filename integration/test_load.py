import os

import pytest
from click.testing import CliRunner
from sqlmodel import select

from dundie.cli import load, main
from dundie.database import get_session
from dundie.models import Person, User
from dundie.utils.db import add_person
from dundie.utils.login import AccessDeniedError

from .constants import (
    DUNDIE_ADMIN_USER,
    DUNDIE_ADMIN_USER_PASSWORD,
    PEOPLE_FILE,
)

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.medium
def test_load_positive_call_load_command():
    """test command load"""

    os.environ["DUNDIE_USER"] = DUNDIE_ADMIN_USER
    os.environ["DUNDIE_PASSWORD"] = DUNDIE_ADMIN_USER_PASSWORD

    out = cmd.invoke(load, PEOPLE_FILE)
    assert "Dunder Mifflin Associates" in out.output


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize("wrong_command", ["loady", "carrega", "start"])
def test_load_negative_call_load_command_with_wrong_params(wrong_command):
    """test command load"""
    out = cmd.invoke(main, wrong_command, PEOPLE_FILE)
    assert out.exit_code != 0
    assert f"No such command '{wrong_command}'." in out.output


@pytest.mark.integration
def test_load_negative_admin_interaction(request):
    """Test function load function."""

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

        out = cmd.invoke(load, PEOPLE_FILE)

        assert out.exit_code != 0
        assert AccessDeniedError
