from pydantic import BaseModel
from sqlmodel import Field, SQLModel

UserID = int

class CreateUserRequest(BaseModel):
    username: str
    password: str
    email: str

class UserResponse(SQLModel):
    id: UserID = Field(primary_key=True)
    verification_code: str = None
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    nickname: str = None
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

