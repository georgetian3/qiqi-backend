from datetime import datetime, timedelta
from typing import Dict

from jose import JWTError, jwt

import models.database
import models.location
import models.user

from services.base import QiQiBaseService

class UserService(QiQiBaseService):

    def decode_token(self, token: str) -> models.user.UserID | None:
        try:
            payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM])
            return payload.get('sub')
        except JWTError:
            return None

    def create_access_token(self, data: Dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
        to_encode = data.copy()
        to_encode.update({'exp': datetime.utcnow() + expires_delta})
        encoded_jwt = jwt.encode(to_encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM)
        return encoded_jwt