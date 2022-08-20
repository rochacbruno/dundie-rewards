<<<<<<< HEAD
"""Config environment variables to email server and path root."""

=======
>>>>>>> 3675e88a678e05be48a17838b5c5f4eb528f7ce5
import os

SMTP_HOST = "localhost"
SMTP_PORT = 8025
SMTP_TIMEOUT = 5
EMAIL_FROM = "master@dundie.com"
ROOT_PATH = os.path.dirname(__file__)
DATABASE_PATH: str = os.path.join(ROOT_PATH, "..", "assets", "database.json")
