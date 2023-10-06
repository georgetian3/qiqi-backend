from sqlmodel import SQLModel, Field

from typing import Optional


DeviceID = int
UserID = int


class Location(SQLModel, table = True):
    __tablename__ = 'location'
    user_id: UserID = Field(primary_key=True)
    location_lat: Optional[float] = None
    location_long: Optional[float] = None