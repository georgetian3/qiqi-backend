import email_validator
import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

async def send_html_email(
    sender: str,
    recipient: list[str],
    subject: str,
    content: str,
    hostname: str,
    port: int,
    username: str,
    password: str,
):

    message = MIMEMultipart('alternative')
    message['From'] = sender
    message['To'] = ', '.join(recipient)
    message['Subject'] = subject
    message.attach(MIMEText(content, 'plain', 'utf-8'))

    return await aiosmtplib.send(
        message=message,
        hostname=hostname,
        port=port,
        username=username,
        password=password,
        use_tls=True
    )

def normalize(email: str) -> str | None:
    try:
        return email_validator.validate_email(email, check_deliverability=False).normalized
    except:
        return None

def is_valid(email: str, check_deliverability=False) -> bool:
    try:
        email_validator.validate_email(email, check_deliverability=check_deliverability)
        return True
    except:
        return False