from random import sample
from string import ascii_letters


def generate_simple_password(size=8):
    return "".join(sample(ascii_letters, size))
