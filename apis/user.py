import fastapi
from models.user import User
import models.user
import models.database
from config import Config

from typing import Optional

import asyncio
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlmodel import Field, SQLModel, create_engine, Session, select, col

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
        
        @self.post('/user')
        async def user():
            return await self.user_service.create_user()
        
        @self.post("/update-user-paramenters/{user_id}")
        async def update_user_paramenters(user_id: int, username: Optional[str] = None, password_hash: Optional[str] = None, email: Optional[str] = None, share_location: Optional[bool] = None, friendlist: Optional[str] = None,):                
            #get user data
            async with self.database.async_session() as session:
                statement = await session.execute(select(User).where(User.id == user_id))
                
                user = statement.one()[0]

                if user.username != None:
                    user.username = username
                if user.password_hash != None:
                    user.password_hash = password_hash
                if user.email != None:
                    user.email = email 
                if user.share_location != None:
                    user.share_location = share_location   
                if user.friendlist != None:
                    user.friendlist = friendlist   

                session.add(user)
                await session.commit()
                session.refresh(user)
            
            return user