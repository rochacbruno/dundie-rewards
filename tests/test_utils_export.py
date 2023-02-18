import os

import pytest

from dundie.core import add_person, read
from dundie.database import get_session
from dundie.models import Person
from dundie.utils.export import export_csv
from tests.constants import PEOPLE_FILE_EXPORT_ERROR, TEST_PATH_OUTPUT


@pytest.mark.unit
def test_export_csv_negative():
    """Test error in file"""

    with get_session() as session:
        joe = {
            "email": "joe@doe.com",
            "name": "Joe Doe",
            "dept": "Sales",
            "role": "Salesman",
        }

        instance_joe = Person(**joe)
        _, created = add_person(session=session, instance=instance_joe)
        assert created is True

        jim = {
            "email": "jim@doe.com",
            "name": "Jim Doe",
            "dept": "Management",
            "role": "Manager",
        }

        instance_jim = Person(**jim)
        _, created = add_person(session=session, instance=instance_jim)
        assert created is True

        session.commit()

        result = read()
        output = PEOPLE_FILE_EXPORT_ERROR

        export_csv(output, result)
        assert PermissionError


@pytest.mark.unit
def test_export_csv_positive():
    """Ensure file make with function"""

    with get_session() as session:
        joe = {
            "email": "joe@doe.com",
            "name": "Joe Doe",
            "dept": "Sales",
            "role": "Salesman",
        }

        instance_joe = Person(**joe)
        _, created = add_person(session=session, instance=instance_joe)
        assert created is True

        jim = {
            "email": "jim@doe.com",
            "name": "Jim Doe",
            "dept": "Management",
            "role": "Manager",
        }

        instance_jim = Person(**jim)
        _, created = add_person(session=session, instance=instance_jim)
        assert created is True

        session.commit()

        result = read()
        output = TEST_PATH_OUTPUT

        export_csv(output, result)

        assert os.path.exists(f"{TEST_PATH_OUTPUT}.csv") is True
