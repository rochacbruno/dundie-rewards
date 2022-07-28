import pytest
from .constants import PEOPLE_FILE
from dundie.core import load


@pytest.mark.unit
@pytest.mark.high
def test_load():
    assert len(load(PEOPLE_FILE)) == 2
    assert load(PEOPLE_FILE)[0][0] == 'J'
