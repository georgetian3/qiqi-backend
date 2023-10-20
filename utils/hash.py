import argon2


def hash(password: str) -> str:
    return argon2.hash_password(bytes(password, 'utf8')).decode()

def verify(hash: str, password: str) -> bool:
    try:
        argon2.verify_password(bytes(hash, 'utf8'), bytes(password, 'utf8'))
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False