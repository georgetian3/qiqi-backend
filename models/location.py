from datetime import datetime

from sqlmodel import Field, SQLModel

DeviceID = int
UserID = int

class Location(SQLModel):
    latitude: float = None
    longitude: float = None
    altitude: float = None

class Area(SQLModel):
    """ Rectangular area defined by Locations of two opposite corners """
    location1: Location
    location2: Location

class UserLocation(Location, table=True):
    __tablename__ = 'location'
    user_id: UserID = Field(primary_key=True, foreign_key='user.id')
    timestamp: datetime