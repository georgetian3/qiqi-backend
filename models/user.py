from pydantic import BaseModel
from sqlmodel import Field, SQLModel

UserID = int

class CreateUserRequest(BaseModel):
    username: str
    password: str

class UserResponse(SQLModel):
    id: UserID = Field(primary_key=True)
    verified: bool = False
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    nickname: str
    share_location: bool

class VerificationCode(SQLModel, table=True):
    user_id: UserID = Field(primary_key=True)
    code: str = Field(unique=True, index=True)

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

