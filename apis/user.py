from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.exceptions import HTTPException

import models.database
import models.location
import models.user
from apis.base import QiQiBaseRouter
from apis.documentedresponse import JDR, JDR204, JDR404, create_documentation
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


        get_user_200 = JDR(status.HTTP_200_OK, JDR204.description, models.user.UserResponse)
        @self.get(
            '/user',
            description='Get user based on either `user_id` or `username` as specified in the query parameters',
            **create_documentation(get_user_200, JDR404),
        )
        async def get_user(user_id: UserID | None = None, username: str | None = None):
            user =  await self.services.user.get_user(user_id, username)
            if user is None:
                return Exception('test')
            return user



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