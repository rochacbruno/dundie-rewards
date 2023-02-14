from random import sample
from string import ascii_letters, digits

from cryptography.fernet import Fernet

from dundie.settings import SECRET_KEY


def generate_simple_password(size: int = 8) -> str:
    """Generate a simple random password
    [A-Z][a-z][0-9]
    """
    password = sample(ascii_letters + digits, size)
    password = password_encrypt(str("".join(password)))

    return password


def password_encrypt(password: str) -> str:
    """Encrypt for password"""

    factory_encrypt = Fernet(SECRET_KEY)

    value = password
    value_bytes = bytes(value, encoding="utf-8")

    token = factory_encrypt.encrypt(value_bytes)
    result = token.decode()

    return result


def password_decrypt(password: str) -> str:
    """Decrypt for password"""

    factory_encrypt = Fernet(SECRET_KEY)

    token = factory_encrypt.decrypt(password)
    result = token.decode()

    return result
