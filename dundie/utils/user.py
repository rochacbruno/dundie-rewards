"""Genarete passwords to users."""
from random import sample
from string import ascii_letters, digits


def generate_simple_password(size=8):
    """Genarate a simple ramdom passaword."""
    password = sample(ascii_letters + digits, size)
    return "".join(password)
