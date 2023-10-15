from datetime import datetime

from sqlmodel import Field, SQLModel

DeviceID = int
UserID = int

class Location(SQLModel):
    latitude: float = None
    longitude: float = None
    altitude: float = None

class UserLocation(Location, table=True):
    __tablename__ = 'location'
    user_id: UserID = Field(primary_key=True, foreign_key='user.id')
    timestamp: datetime