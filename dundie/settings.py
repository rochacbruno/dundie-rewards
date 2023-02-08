import os

SMTP_HOST: str = "localhost"
SMTP_PORT: int = 8025
SMTP_TIMEOUT: int = 5

EMAIL_FROM: str = "master@dundie.com"
DATEFMT: str = "%d/%m/%Y %H:%M:%S"
API_BASE_URL: str = (
    "https://economia.awesomeapi.com.br/json/last/USD-{currency}"
)

ROOT_PATH: str = os.path.dirname(__file__)
DATABASE_PATH: str = os.path.join(ROOT_PATH, "..", "assets", "database.db")
SQL_CON_STRING = f"sqlite:///{DATABASE_PATH}"

DUNDIE_ADMIN_USER: str = "michael@dundermifflin.com"
DUNDIE_ADMIN_USER_PASSWORD: str = """gAAAAABj4a-ksOTbTEvQmMh6Gjr9tCFv4u_
Sis0FnMiBh6ahbESAL3qb_VFn-ZNxVpcfXOJ51B5JCKXNaJ36yeyd9_3WrG0zZA=="""

SECRET_KEY: bytes = b"r184HKiupQ6hbzf8zMKQXDWQkUIRddKcbkEqOt1M9RM="
