<<<<<<< HEAD
=======
"""Test utils."""
>>>>>>> projeto-dundie-rewards/main
import pytest

from dundie.utils.email import check_valid_email
from dundie.utils.user import generate_simple_password


@pytest.mark.unit
@pytest.mark.parametrize(
<<<<<<< HEAD
    "address", ["bruno@rocha.com", "joe@doe.com", "a@b.pt"]
=======
    "address", ["figueiredovt@yahoo.com.br", "joe@doe.com", "a@b.pt"]
>>>>>>> projeto-dundie-rewards/main
)
def test_positive_check_valid_email(address):
    """Ensure email is valid."""
    assert check_valid_email(address) is True


@pytest.mark.unit
<<<<<<< HEAD
@pytest.mark.parametrize("address", ["bruno@.com", "@doe.com", "a@b"])
=======
@pytest.mark.parametrize(
    "address", ["figueiredovtyahoo.com.br", "@doe.com", "a@b"]
)
>>>>>>> projeto-dundie-rewards/main
def test_negative_check_valid_email(address):
    """Ensure email is invalid."""
    assert check_valid_email(address) is False


@pytest.mark.unit
def test_generate_simple_password():
<<<<<<< HEAD
    """Test generation of random simple passwords
    TODO: Generate hashed complex passwords, encrypit it
=======
    """Test generation of ramdom simple passwords."""
    """
    TODO: Generation hashed complex passwords, encrypit it
>>>>>>> projeto-dundie-rewards/main
    """
    passwords = []
    for _ in range(100):
        passwords.append(generate_simple_password(8))
<<<<<<< HEAD

=======
>>>>>>> projeto-dundie-rewards/main
    assert len(set(passwords)) == 100
