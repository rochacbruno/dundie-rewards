import pytest

from dundie.database import connect, EMPTY_DB
from dundie.core import load
from .constants import PEOPLE_FILE


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_has_3_people():
    """Test function load function."""
    assert len(load(PEOPLE_FILE)) == 3


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_first_name_starts_with_j():
    """Test function load function."""
    assert load(PEOPLE_FILE)[0]["name"][0] == "J"


@pytest.mark.unit
def test_db_schema():
    load(PEOPLE_FILE)
    db = connect()
    assert db.keys() == EMPTY_DB.keys()
