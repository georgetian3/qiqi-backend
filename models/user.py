from typing import Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Token(BaseModel):
    access_token: str
    token_type: str

UserID = int

class User(SQLModel, table=True):
    __tablename__ = 'user'
    id: UserID = Field(primary_key=True)
    username: str = Field(unique=True, index=True)
    password_hash: str
    nickname: str
    email: str
    share_location: bool = True

class Friend(SQLModel, table=True):
    __tablename__ = 'friend'
    user1: UserID = Field(primary_key=True)
    user2: UserID = Field(primary_key=True)

class FriendRequestDB(SQLModel, table=True):
    __tablename__ = 'friend_request'
    user1: UserID = Field(primary_key=True)
    user2: UserID = Field(primary_key=True)

class FriendRequest(BaseModel):
    friend_id: UserID

class CreateUserRequest(BaseModel):
    username: str
    password: str