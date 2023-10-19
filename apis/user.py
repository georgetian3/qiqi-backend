from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException

import models.user
import models.database
import models.location
from apis.base import QiQiBaseRouter
from models.user import Token, UserID

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

class UserApi(QiQiBaseRouter):
    """ User API """

    def get_current_user(self, token: str = Depends(oauth2_scheme)) -> models.user.User | None:
            user_id = self.services.user.decode_token(token)
            if user_id is None:
                raise self.credentials_exception
            return user_id

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        @self.post('/token', response_model=Token)
        async def token(form_data: OAuth2PasswordRequestForm = Depends()):
            user = await self.services.user.authenticate(form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Incorrect username or password',
                    headers={'WWW-Authenticate': 'Bearer'},
                )
            access_token = self.services.user.create_access_token({'sub': user.id})
            return {'access_token': access_token, 'token_type': 'bearer'}

        @self.get('/user/{id}')
        async def get_user_by_id(id: UserID):
            return await self.services.user.get_user(user_id=id)
        
        @self.get('/user/{username}')
        async def get_user_by_username(username: str):
            return await self.services.user.get_user(username=username)


        self.credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        
        
        @self.put('/user', description='Create a new user')
        async def create_user(details: models.user.CreateUserRequest):
            return await self.services.user.create_user(details)
        
        @self.patch('/user')
        async def update_user():
            return await self.services.user.update_user()
        
        @self.get('/friends')
        async def get_friends(user):
            await self.services.user.get_friends()

        @self.put('/friends')
        async def send_friend_request():
            ...

        @self.patch('/friends')
        async def accept_friend_request():
            ...

        @self.delete('/friends')
        async def delete_friend():
            ...