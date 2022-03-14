import re
import smtplib
from email.mime.text import MIMEText

from dundie.utils.log import get_logger

log = get_logger()


regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


def check_valid_email(address):
    """Verifies if an email address is valid."""
    if re.fullmatch(regex, address):
        return True
    else:
        return False


def send_email(from_, to, subject, text):
    try:
        with smtplib.SMTP(host="localhost", port=8025, timeout=5) as server:
            message = MIMEText(text)
            message["Subject"] = subject
            message["From"] = from_
            message["To"] = to
            server.sendmail(from_, to, message.as_string())
    except Exception:
        log.error("cannot send email")
