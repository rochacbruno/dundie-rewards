import pytest

from dundie.core import load

from .constants import PEOPLE_FILE, PEOPLE_FILE_ERROR


@pytest.mark.unit
def test_load_positive_has_2_people(request):
    """Test function load function."""
    assert len(load(PEOPLE_FILE)) == 3


@pytest.mark.unit
def test_load_positive_first_name_starts_with_j(request):
    """Test function load function."""
    assert load(PEOPLE_FILE)[0]["name"] == "Jim Halpert"


@pytest.mark.unit
def test_load_negative_load_not_found(request):
    """Test function load function."""
    with pytest.raises(FileNotFoundError):
        load(PEOPLE_FILE_ERROR)
