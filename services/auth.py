from datetime import datetime, timedelta
from typing import Dict

from jose import JWTError, jwt

import models.database
import models.location
import models.user
from services.base import QiQiBaseService


class AuthService(QiQiBaseService):

    def decode_token(self, token: str) -> models.user.UserID | None:
        try:
            payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM])
            return models.user.UserID(payload.get('sub'))
        except JWTError:
            return None

    def create_access_token(self, user_id: models.user.UserID, expires_delta: timedelta = timedelta(minutes=15)) -> str:
        return jwt.encode(
            {
                'exp': datetime.utcnow() + expires_delta,
                'sub': str(user_id)
            },
            self.config.SECRET_KEY, algorithm=self.config.ALGORITHM,
        )