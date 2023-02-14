import pytest

from dundie.utils.email import check_valid_email


@pytest.mark.unit
@pytest.mark.medium
@pytest.mark.parametrize(
    "address", ["jose@gmail.com", "joe@doe.com", "a@b.pt"]
)
def test_positive_check_valid_email(address):
    """Ensure email is valid."""
    assert check_valid_email(address) is True


@pytest.mark.unit
@pytest.mark.medium
@pytest.mark.parametrize("address", ["jose@.com", "@doe.com", "a@b"])
def test_negative_check_valid_email(address):
    """Ensure email is invalid."""
    assert check_valid_email(address) is False
