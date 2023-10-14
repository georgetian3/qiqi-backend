from datetime import datetime, timedelta
from typing import Dict
from jose import JWTError, jwt
import models.user
import argon2
import sqlalchemy

from models.database import QiQiDatabase
from config import QiQiConfig

class AuthService:
    """ Auth service """

    def __init__(self, database: QiQiDatabase, config: QiQiConfig):
        self.config = config
        self.database = database

    async def authenticate(self, username: str, password: str) -> bool:
        """
        Returns: True if password matches username, False if password does not match username or if username is not found
        """
        async with self.database.async_session() as session:
            user: models.user.User = await session.scalar(sqlalchemy.select(models.user.User).where(models.user.User.username == username))
        if user is None:
            return False
        try:
            argon2.verify_password(bytes(user.password_hash), bytes(password))
            return True
        except argon2.exceptions.VerifyMismatchError:
            return False

    def create_access_token(self, data: Dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
        to_encode = data.copy()
        to_encode.update({'exp': datetime.utcnow() + expires_delta})
        encoded_jwt = jwt.encode(to_encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM)
        return encoded_jwt
    
    async def get_current_user(self, token: str) -> UserID | None:
        try:
            payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM])
            username: str = payload.get('sub')
            if username is None:
                return None
        except JWTError:
            return None
        user = get_user(fake_users_db, username=token_data.username)
        if user is None:
            return None
        return user
    