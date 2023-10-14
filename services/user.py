import models.user
import models.database
import models.location

from typing import Optional

from sqlmodel import select

from config import QiQiConfig

import sqlalchemy

class UserService:

    def __init__(self, database: models.database.QiQiDatabase, config: QiQiConfig):
        self.config = config
        self.database = database

    async def create_user(self) -> models.user.User:
        new_user = models.user.User(
            username='user15',
            password_hash='testpwhash',
            email='oo@mail.com',
            share_location=False
        )
        user_location_field = models.location.Location(
            location_lat=0,
            location_long=0
        )
        # TypeError: 'Session' object does not support the asynchronous context manager protocol
        async with self.database.async_session() as session:
            session.add(new_user)
            session.add(user_location_field)
            await session.commit()
        return new_user

    async def get_user(self, id_or_username: models.user.UserID | str) -> models.user.User:
        if isinstance(id_or_username, models.user.UserID):
            ...
        return models.user.User(
                id=0,
                usernaname='test',
                password_hash=None,
                email='test@georgetian.com'
        )
    
    async def update_share_location_status(self, user_id: int, share_location: bool):
        async with self.database.async_session() as session:
            statement = await session.execute(select(models.location.Location).where(models.location.Location.user_id == user_id))

            user_location_var = statement.one()[0]
            
            user_location_var.share_location = share_location

            session.add(user_location_var)
            await session.commit()
        
        return 'successfully set share_location to {}'.format(share_location)
    
    async def update_user(self, user_id: int, userClass: models.user.UpdateUser):
        async with self.database.async_session() as session:
            statement = await session.execute(select(models.user.User).where(models.user.User.id == user_id))
            
            user = statement.one()[0]

            if userClass.username != None:
                user.username = userClass.username
            if userClass.password_hash != None:
                user.password_hash = userClass.password_hash
            if userClass.email != None:
                user.email = userClass.email 
            if userClass.friendlist != None:
                user.friendlist = userClass.friendlist   

            session.add(user)
            await session.commit()

        return 'update user variable success'
    
    async def add_friend(self, user_id, friend_user_name):
        #find friend's user id
        async with self.database.async_session() as session:
            try:
                #find friend's id with username
                statement = await session.execute(select(models.user.User).where(models.user.User.username == friend_user_name))
                friend = statement.one()[0]

                #add friend's id to user
                user_statement = await session.execute(select(models.user.User).where(models.user.User.id == user_id))
                user = user_statement.one()[0]
                print(user.friendlist)
                if user.friendlist == None and friend.friendlist == None:
                    user.friendlist = "{}".format(friend.id)
                    friend.friendlist = "{}".format(user_id)
                    await session.commit()
                    return 'Friend with name {} successfully added!'.format(friend_user_name)
                if friend.friendlist == None:
                    user.friendlist = user.friendlist + ",{}".format(friend.id)
                    friend.friendlist = "{}".format(user_id)
                    await session.commit()
                    return 'Friend with name {} successfully added!'.format(friend_user_name)
                if user.friendlist == None:
                    user.friendlist = "{}".format(friend.id)
                    friend.friendlist = friend.friendlist + ",{}".format(user.id)
                    await session.commit()
                    return 'Friend with name {} successfully added!'.format(friend_user_name)
                else:
                    friendlist = user.friendlist
                    friendlist = friendlist.split(",")
                    for i in friendlist:
                        if int(i) == int(friend.id):
                            return 'This user is already your friend!'
                    else:
                        user.friendlist = user.friendlist + ",{}".format(friend.id)
                        friend.friendlist = friend.friendlist + ",{}".format(friend.id)
                        await session.commit()
                        return 'Friend with name {} successfully added!'.format(friend_user_name)
            except sqlalchemy.exc.NoResultFound:
                return 'User with that name does not exist!'

            
    async def add_friend_request(self, user_id, friend_id):
        ...