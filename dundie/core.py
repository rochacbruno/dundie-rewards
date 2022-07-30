"""Core module for dundie - (controler or base or paste load)"""
from dundie.utils.log import get_logger

log = get_logger()


def load(filepath):
    """ Loads data from filepath to the database.
    #python -m doctest -v dundie/core.py

    >>> len(load('assets/people.csv'))
    2

    """
    try:
        with open(filepath) as file_:
            return [line.strip() for line in file_.readlines()]
            """for line in file_:
                print(line)
"""
    except FileNotFoundError as e:
        log.error(str(e))
