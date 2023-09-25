from datetime import datetime, timedelta
from typing import Annotated, Dict
from jose import JWTError, jwt
import models.user
from config import Config

class AuthService:
    def __init__(self, config: Config):
        self.config = config

    async def authenticate(username: str, password, str) -> models.user.User:
        ...

    def create_access_token(self, data: Dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
        to_encode = data.copy()
        to_encode.update({'exp': datetime.utcnow() + expires_delta})
        encoded_jwt = jwt.encode(to_encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM)
        return encoded_jwt
    
    async def get_current_user(self, token: str):
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