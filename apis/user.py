import fastapi
from fastapi import status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
import sqlalchemy
from models.user import Token
import models.database
import models.location
from apis.base import QiQiBaseApi
from starlette.exceptions import HTTPException
from typing import Annotated, Optional

from models.user import UserID

class UserApi(QiQiBaseApi):
    """ User API """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

        @self.post('/token', response_model=Token)
        async def token(
            form_data: Annotated[OAuth2PasswordRequestForm, fastapi.Depends()]
        ):
            user = await self.services.user.authenticate(form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Incorrect username or password',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            access_token = self.services.user.create_access_token({'sub': user.id})
            return {'access_token': access_token, 'token_type': 'bearer'}

        async def get_current_user(self, token: str) -> models.user.User | None:
            try:
                payload = JWTError.decode(token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM])
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

        @self.get('/user')
        async def user():
            return 'user'
        
        @self.put('/user')
        async def create_user():
            return await self.services.user.create_user()
        
        @self.patch('/user')
        async def update_user():
            return await self.services.user.update_user()
        
        @self.get('/friends')
        async def get_friends(user):
            await self.services.user.get_friends()

        @self.patch('/friends')
        async def send_friend_request():
            ...

        @self.put('/friends')
        async def accept_friend_request():
            ...

        @self.delete('/friends')
        async def delete_friend():
            ...