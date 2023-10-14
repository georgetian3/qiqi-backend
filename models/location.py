from sqlmodel import SQLModel, Field

DeviceID = int
UserID = int


class Location(SQLModel):
    latitude: float = None
    longitude: float = None
    altitude: float = None

class LocationDB(Location, table=True):
    __tablename__ = 'location'
    user_id: UserID = Field(primary_key=True)
    timestamp: int