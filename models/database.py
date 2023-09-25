import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from sqlmodel import SQLModel

from models.auth import *
from models.user import *
from models.location import *

import nest_asyncio
nest_asyncio.apply()



class Database:
    def __init__(self, database_url: str):
        self.engine = create_async_engine(database_url)
        self.async_session = sessionmaker(self.engine)
        self.is_sqlite = 'sqlite' in database_url

        async def _sqlite_foreign_keys():
            async with self.engine.connect() as conn:
                if 'sqlite' in database_url:
                    await conn.execute(text('PRAGMA foreign_keys=ON'))
                    await conn.commit()

        asyncio.run(_sqlite_foreign_keys())

    def reset(self):
        async def _reset():
            async with self.engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.drop_all)
                await conn.run_sync(SQLModel.metadata.create_all)
        asyncio.run(_reset())