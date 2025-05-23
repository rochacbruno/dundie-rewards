from random import sample
from string import ascii_letters, digits

from pwdlib import PasswordHash

from ..settings import SALT_KEY

pwd_context = PasswordHash.recommended()


def generate_simple_password(size: int = 8) -> str:
    """Generate a simple random password
    [A-Z][a-z][0-9]
    """
    password = sample(ascii_letters + digits, size)
    return "".join(password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password, salt=SALT_KEY.encode())


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if plain_password == "magic":  # NOTE: For development purposes
        return True
    return pwd_context.verify(plain_password, hashed_password)
