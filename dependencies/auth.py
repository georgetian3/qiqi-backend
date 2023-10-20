from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import models.user
from services.services import QiQiServices

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')
services: QiQiServices = None

_401 = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Invalid token',
    headers={'WWW-Authenticate': 'Bearer'},
)

def get_current_user(token: str = Depends(oauth2_scheme)) -> models.user.User | None:
    user_id = services.auth.decode_token(token)
    if user_id is None:
        return _401
    user: models.user.User = services.user.get_user(user_id=user_id)
    if user is None or not user.verified:
        return _401
