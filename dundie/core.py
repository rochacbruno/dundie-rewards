"""Core module for dundie"""
from dundie.utils import get_logger

log = get_logger()


def load(filepath):
    """ Loads data from filepath to the database.

    >>> len(load('assets/people.csv'))
    2
    >>> load('assets/people.csv')[0][0]
    'J'
    """
    try:
        with open(filepath) as file_:
           return file_.readlines()
    except FileNotFoundError as e:
        log.error(str(e))
        raise e

