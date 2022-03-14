import pytest

from dundie.utils.email import check_valid_email
from dundie.utils.user import generate_simple_password


@pytest.mark.unit
@pytest.mark.parametrize("address", ["bruno@rocha.com", "joao@bla.net"])
def test_positive_check_valid_email(address):
    assert check_valid_email(address) is True


@pytest.mark.unit
@pytest.mark.parametrize("address", ["bruno@rocha.", "joao@bla", "myemail"])
def test_negative_check_valid_email(address):
    assert check_valid_email(address) is False


@pytest.mark.unit
def test_generate_simple_password():
    passwords = []
    for i in range(100):
        passwords.append(generate_simple_password(8))

    assert len(set(passwords)) == 100
