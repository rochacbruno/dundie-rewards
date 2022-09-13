import pytest
from click.testing import CliRunner

from dundie.cli import load, main
<<<<<<< HEAD

from .constants import PEOPLE_FILE
=======
from tests.constants import PEOPLE_FILE
>>>>>>> projeto-dundie-rewards/main

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.medium
def test_load_positive_call_load_command():
<<<<<<< HEAD
    """test command load"""
    out = cmd.invoke(load, PEOPLE_FILE)
    assert "Dunder Mifflin Associates" in out.output
=======
    """Test command load."""
    out = cmd.invoke(load, PEOPLE_FILE)

    assert "LOGIN: " in out.output
>>>>>>> projeto-dundie-rewards/main


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize("wrong_command", ["loady", "carrega", "start"])
def test_load_negative_call_load_command_with_wrong_params(wrong_command):
<<<<<<< HEAD
    """test command load"""
    out = cmd.invoke(main, wrong_command, PEOPLE_FILE)
    assert out.exit_code != 0
=======
    """Test command load."""
    out = cmd.invoke(main, wrong_command, PEOPLE_FILE)

    assert out.output != 0
>>>>>>> projeto-dundie-rewards/main
    assert f"No such command '{wrong_command}'." in out.output
