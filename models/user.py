from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Token(BaseModel):
    access_token: str
    token_type: str

UserID = int

class CreateUserRequest(BaseModel):
    username: str
    password: str

class UserResponse(SQLModel):
    id: UserID = Field(primary_key=True)
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    nickname: str
    share_location: bool

class User(UserResponse, table=True):
    __tablename__ = 'user'
    password_hash: str

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

