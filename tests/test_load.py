import pytest
from dundie.core import load
from .constants import PEOPLE_FILE


@pytest.mark.unit
@pytest.mark.high
def test_load():
    """Test function load function."""
    assert len(load(PEOPLE_FILE)) == 2
    assert load(PEOPLE_FILE)[0][0] == 'J'
    