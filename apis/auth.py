import fastapi
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from models.auth import Token
from services.auth import AuthService
from typing import Annotated
from starlette.exceptions import HTTPException
from jose import jwt
from apis.base import QiQiBaseApi

class AuthApi(QiQiBaseApi):
    """ Auth API """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

        @self.post('/token', response_model=Token)
        async def token(
            form_data: Annotated[OAuth2PasswordRequestForm, fastapi.Depends()]
        ):
            user = await self.services.auth.authenticate(form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Incorrect username or password',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            access_token = self.services.auth.create_access_token({'sub': user.id})
            return {'access_token': access_token, 'token_type': 'bearer'}


        async def get_current_user(self, token: str) -> models.user.User | None:
            try:
                payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM])
                user_id: UserID = payload.get('sub')
                if user_id is None:
                    return None
            except JWTError:
                return None
            async with self.database.async_session() as session:
                user = session.scalar(sqlalchemy.select(models.user.User).where(models.user.User.id == id))
            if user is None:
                return None
            return user

        async def get_current_user(token: Annotated[str, Depends(self.oauth2_scheme)]):
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Could not validate credentials',
                headers={'WWW-Authenticate': 'Bearer'},
            )
            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username: str = payload.get('sub')
                if username is None:
                    raise credentials_exception
                token_data = TokenData(username=username)
            except JWTError:
                raise credentials_exception
            user = get_user(fake_users_db, username=token_data.username)
            if user is None:
                raise credentials_exception
            return user



