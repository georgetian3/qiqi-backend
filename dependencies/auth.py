from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

import models.user
import services.auth

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/token')
auth_service: services.auth.AuthService = None
def get_current_user(token: str = Depends(oauth2_scheme)) -> models.user.User | None:
    user_id = auth_service.decode_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    return user_id