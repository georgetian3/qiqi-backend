from sqlmodel import SQLModel, Field

from typing import Optional

UserID = int

class User(SQLModel, table=True):
    __tablename__ = 'user'
    id: UserID = Field(primary_key=True)
    username: str = Field(index=True)
    password_hash: str
    email: str
    friendlist: Optional[str] = None

class UpdateUser(SQLModel, table=True):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    username: Optional[str]
    password_hash: Optional[str]
    email: Optional[str]
    friendlist: Optional[str] = None