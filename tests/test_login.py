import pytest

from dundie.core import AuthenticationError, load, login

from .constants import PEOPLE_FILE


@pytest.mark.unit
def test_negative_login():
    with pytest.raises(AuthenticationError):
        login("me@me.com", "123456")


@pytest.mark.unit
def test_positive_login():
    load(PEOPLE_FILE)
    person = login("jim@dundlermifflin.com", "FohtY0TC")
    assert person[0].email == "jim@dundlermifflin.com"
