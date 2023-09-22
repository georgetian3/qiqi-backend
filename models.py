from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine



class Location(SQLModel):
    latitude: float
    longitude: float

class UserLocation(Location):
    user: int





def reset_db(engine: AsyncEngine):
    SQLModel.metadata.create_all(engine)