import argon2

def hash(password: str) -> str:
    return argon2.hash_password(bytes(password)).decode()

def verify(hash: str, password: str) -> bool:
    try:
        argon2.verify_password(bytes(hash), bytes(password))
        return True
    except argon2.exceptions.VerifyMismatchError:
        return False