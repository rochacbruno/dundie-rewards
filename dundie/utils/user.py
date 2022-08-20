<<<<<<< HEAD
"""Genarete passwords to users."""
=======
>>>>>>> 3675e88a678e05be48a17838b5c5f4eb528f7ce5
from random import sample
from string import ascii_letters, digits


def generate_simple_password(size=8):
<<<<<<< HEAD
    """Genarate a simple ramdom passaword."""
=======
    """Genarate a simple ramdom passaword"""
>>>>>>> 3675e88a678e05be48a17838b5c5f4eb528f7ce5
    password = sample(ascii_letters + digits, size)
    return "".join(password)
