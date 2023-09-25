""" """

from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine


DeviceID = int
UserID = int


class Location(SQLModel):
    """ """
    user_id: UserID
    latitude: float
    longitude: float
