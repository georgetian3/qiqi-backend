import email_validator

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