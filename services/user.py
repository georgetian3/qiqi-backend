from datetime import datetime, timedelta
from typing import Dict, List

import argon2
import sqlalchemy
from jose import JWTError, jwt
from sqlmodel import select

import models.database
import models.location
import models.user
from config import QiQiConfig


class UserService:

    def __init__(self, database: models.database.QiQiDatabase, config: QiQiConfig):
        self.config = config
        self.database = database

    async def decode_token(self, token: str) -> models.user.UserID | None:
        try:
            payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=[self.config.ALGORITHM])
            return payload.get('sub')
        except JWTError:
            return None

    async def hash(self, password: str) -> str:
        return argon2.hash_password(bytes(password)).decode()

    async def authenticate(self, username: str, password: str) -> models.user.User | None:
        """
        Returns: True if password matches username, False if password does not match username or if username is not found
        """
        async with self.database.async_session() as session:
            user: models.user.User = await session.scalar(sqlalchemy.select(models.user.User).where(models.user.User.username == username))
        if user is None:
            return None
        try:
            argon2.verify_password(bytes(user.password_hash), bytes(password))
            return user
        except argon2.exceptions.VerifyMismatchError:
            return None

    def create_access_token(self, data: Dict, expires_delta: timedelta = timedelta(minutes=15)) -> str:
        to_encode = data.copy()
        to_encode.update({'exp': datetime.utcnow() + expires_delta})
        encoded_jwt = jwt.encode(to_encode, self.config.SECRET_KEY, algorithm=self.config.ALGORITHM)
        return encoded_jwt

    async def create_user(self, details: models.user.CreateUserRequest) -> models.user.User | Exception:
        new_user = models.user.User(
            username=details.username,
            password_hash=self.hash(details.password),
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

    async def get_user(self, user_id: models.user.UserID = None, username: str = None) -> models.user.User | None:
        if user_id is None and username is None:
            return None
        async with self.database.async_session() as session:
            user = await session.scalar(
                sqlalchemy.select(models.user.User)
                    .where(models.user.User.id == user_id if username is None else models.user.User.username == username)
            )
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
            statement = await session.execute(select(models.location.Location).where(models.location.Location.user_id == user_id))

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