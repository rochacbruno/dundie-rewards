import pytest
from tests.constants import PEOPLE_FILE
from dundie.core import load


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_has_2_people(request):
    assert len(load(PEOPLE_FILE)) == 3

@pytest.mark.unit
@pytest.mark.high
def test_load_positive_first_starts_with_j(request):
    assert load(PEOPLE_FILE)[0][0] == 'J'
