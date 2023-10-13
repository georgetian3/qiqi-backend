from sqlmodel import SQLModel, Field

from typing import Optional


DeviceID = int
UserID = int


class Location(SQLModel):
    latitude: float = None
    longitude: float = None
    altitude: float = None

class LocationDB(Location, table=True):
    __tablename__ = 'location'
    user_id: UserID = Field(primary_key=True)
    
class UpdateShareLocation(SQLModel, table=True):
    __tablename__ = 'location'
    __table_args__ = {'extend_existing': True}
    share_location: Optional[bool] = False
