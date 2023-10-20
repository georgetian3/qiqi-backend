from datetime import datetime, timedelta
from typing import Dict, List

import argon2
import sqlalchemy
from jose import JWTError, jwt

import models.database
import models.location
import models.user
import utils.email
import utils.hash
from services.base import QiQiBaseService


class UserService(QiQiBaseService):

    async def authenticate(self, username_or_email: str, password: str) -> models.user.User | None:
        """
        Returns: User instance if password matches username, else None
        """
        if utils.email.is_valid(username_or_email):
            user = await self.get_user(email=username_or_email)
        else:
            user = await self.get_user(username=username_or_email)
        if user is None:
            return None
        return user if utils.hash.verify(user.password_hash, password) else None

    async def create_user(self, details: models.user.CreateUserRequest) -> models.user.User | Exception:
        new_user = models.user.User(
            username=details.username,
            password_hash=utils.hash.hash(details.password),
            email='',
            share_location=False
        )

        async with self.database.async_session() as session:
            session.add(new_user)
            try:
                await session.commit()
            except Exception as e:
                return e
            # user_location = models.location.UserLocation(user_id=new_user.id)
            # await session.commit()

        return new_user
    
    async def verify(self, code) -> bool:
        ...

    async def get_user(self, user_id: models.user.UserID = None, username: str = None, email: str = None) -> models.user.User | None:
        s = set([user_id, username, email])
        if len(s) != 2 or None not in s: # ensures only one parameter is filled and the rest is `None`
            return None
        if user_id is not None:
            where = models.user.User.id == user_id
        elif username is not None:
            where = models.user.User.username == username
        else:
            where = models.user.User.email == email
        async with self.database.async_session() as session:
            user = await session.scalar(sqlalchemy.select(models.user.User).where(where))
        return user
    
    async def get_friends(self, user_id: models.user.UserID) -> List[models.user.User]:
        async with self.database.async_session() as session:
            friends = list((friend.user1, friend.user2) for friend in session.execute(
                sqlalchemy.select(models.user.Friend)
                    .where(sqlalchemy.or_(
                        models.user.Friend.user1 == user_id,
                        models.user.Friend.user2 == user_id,
                    )
                )
            ))
        
        

    async def update_share_location_status(self, user_id: int, share_location: bool):
        async with self.database.async_session() as session:
            statement = await session.execute(sqlalchemy.select(models.location.Location).where(models.location.Location.user_id == user_id))

            user_location_var = statement.one()[0]
            
            user_location_var.share_location = share_location

            session.add(user_location_var)
            await session.commit()
        
        return 'successfully set share_location to {}'.format(share_location)
    
    # async def update_user(self, user_id: int, userClass: models.user.UpdateUser):
    #     async with self.database.async_session() as session:
    #         statement = await session.execute(select(models.user.User).where(models.user.User.id == user_id))
            
    #         user = statement.one()[0]

    #         if userClass.username != None:
    #             user.username = userClass.username
    #         if userClass.password_hash != None:
    #             user.password_hash = userClass.password_hash
    #         if userClass.email != None:
    #             user.email = userClass.email 
    #         if userClass.friendlist != None:
    #             user.friendlist = userClass.friendlist   

    #         session.add(user)
    #         await session.commit()

    #     return 'update user variable success'
    
    async def add_friend(self, user_id, friend_user_name):
        #find friend's user id
        async with self.database.async_session() as session:
            try:
                #find friend's id with username
                statement = await session.execute(sqlalchemy.select(models.user.User).where(models.user.User.username == friend_user_name))
                friend = statement.one()[0]

                #add friend's id to user
                user_statement = await session.execute(sqlalchemy.select(models.user.User).where(models.user.User.id == user_id))
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