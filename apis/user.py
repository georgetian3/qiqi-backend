import fastapi

from models.user import UpdateUser
import models.user
import models.database
import models.location

from config import Config

from typing import Optional

config = Config()
db = models.database.Database(config.DATABSE_URL)

class UserApi(fastapi.FastAPI):
    """ User API """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = config
        self.database = db
        
        @self.get('/user')
        async def user():
            return 'user'
        
        @self.get('/update')
        async def user():
            return await self.user_service.create_user()
        
        @self.post("/update_share_location_status/{user_id}",)
        async def update_share_location_status(user_id: int, share_location: Optional[bool] = False):
            return await self.user_service.update_share_location_status(user_id, share_location)
        
        @self.post("/update_user/{user_id}", response_model=UpdateUser)
        async def update_user(user_id: int, userClass: UpdateUser):                
            return await self.user_service.update_user(user_id, userClass)
        
        @self.post("/add_friend/{user_id}")
        async def add_friend(user_id: int, friend_username: str):                
            return await self.user_service.add_friend(user_id, friend_username)