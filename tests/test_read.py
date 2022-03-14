import pytest
from dundie.core import read, load
from .constants import PEOPLE_FILE


@pytest.mark.unit
def test_read_all_data():
    load(PEOPLE_FILE)
    result = read()
    assert len(result) == 3


@pytest.mark.unit
def test_read_only_one_dept():
    load(PEOPLE_FILE)
    result = read(dept="Sales")
    assert len(result) == 2


@pytest.mark.unit
def test_read_only_one_person():
    load(PEOPLE_FILE)
    result = read(email="jim@dundlermifflin.com")
    assert len(result) == 1
