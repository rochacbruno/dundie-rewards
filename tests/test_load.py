import pytest

from dundie.core import load
<<<<<<< HEAD

from .constants import PEOPLE_FILE
=======
from tests.constants import PEOPLE_FILE
>>>>>>> projeto-dundie-rewards/main


@pytest.mark.unit
@pytest.mark.high
def test_load_positive_has_2_people(request):
<<<<<<< HEAD
    """Test function load function."""
    assert len(load(PEOPLE_FILE)) == 3
=======
    assert len(load(PEOPLE_FILE)) == 2
>>>>>>> projeto-dundie-rewards/main


@pytest.mark.unit
@pytest.mark.high
<<<<<<< HEAD
def test_load_positive_first_name_starts_with_j(request):
    """Test function load function."""
    assert load(PEOPLE_FILE)[0]["name"] == "Jim Halpert"
=======
def test_load_positive_first_starts_with_j(request):
    assert load(PEOPLE_FILE)[0]["name"] == "Jim Helpert"
>>>>>>> projeto-dundie-rewards/main
