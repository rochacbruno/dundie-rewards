<<<<<<< HEAD
=======
"""Genarete passwords to users."""
>>>>>>> projeto-dundie-rewards/main
from random import sample
from string import ascii_letters, digits


<<<<<<< HEAD
def generate_simple_password(size: int = 8) -> str:
    """Generate a simple random password
    [A-Z][a-z][0-9]
    """
=======
def generate_simple_password(size=8):
    """Genarate a simple ramdom passaword."""
>>>>>>> projeto-dundie-rewards/main
    password = sample(ascii_letters + digits, size)
    return "".join(password)
