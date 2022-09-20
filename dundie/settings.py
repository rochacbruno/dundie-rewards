"""Config environment variables to email server and path root."""
import os

SMTP_HOST: str = "localhost"
SMTP_PORT: int = 8025
SMTP_TIMEOUT: int = 5
API_BASE_URL: str = (
    "https://economia.awesomeapi.com.br/json/last/USD-{currency}"
)
EMAIL_FROM: str = "master@dundie.com"
DATEFMT: str = "%d/%m/%Y %H:%M:%S"
ROOT_PATH: str = os.path.dirname(__file__)
DATABASE_PATH: str = os.path.join(ROOT_PATH, "..", "assets", "database.db")
SQL_CON_STRING = f"sqlite:///{DATABASE_PATH}"
