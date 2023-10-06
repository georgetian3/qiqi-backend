from sqlmodel import SQLModel, Field

from typing import Optional

UserID = int



class User(SQLModel, table=True):
    __tablename__ = 'user'
    id: UserID = Field(primary_key=True)
    username: str = Field(index=True)
    password_hash: str
    email: str
    location_lat: Optional[float] = None
    location_long: Optional[float] = None
    share_location: bool = False
    friendlist: Optional[str] = None