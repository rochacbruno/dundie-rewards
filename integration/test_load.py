import pytest
from click.testing import CliRunner

from dundie.cli import load, main
from tests.constants import PEOPLE_FILE

cmd = CliRunner()


@pytest.mark.integration
@pytest.mark.medium
def test_load_positive_call_load_command():
    """Test command load."""
    out = cmd.invoke(load, PEOPLE_FILE)

    assert "LOGIN: " in out.output


@pytest.mark.integration
@pytest.mark.medium
@pytest.mark.parametrize("wrong_command", ["loady", "carrega", "start"])
def test_load_negative_call_load_command_with_wrong_params(wrong_command):
    """Test command load."""
    out = cmd.invoke(main, wrong_command, PEOPLE_FILE)

    assert out.output != 0
    assert f"No such command '{wrong_command}'." in out.output
