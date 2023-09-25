import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_session
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
        print('----------------engine', self.engine, type(self.engine))
        self.async_session = sessionmaker(self.engine)
        print('---------------------------------session', self.async_session, type(self.async_session))

        self.is_sqlite = 'sqlite' in database_url

        async def _sqlite_foreign_keys():
            async with self.async_session as session:
                if 'sqlite' in database_url:
                    await session.execute('PROGMA foreign_keys=ON')
                    await session.commit()

        asyncio.run(_sqlite_foreign_keys())

    def reset(self):
        async def _reset():
            async with self.engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.drop_all)
                await conn.run_sync(SQLModel.metadata.create_all)
        asyncio.run(_reset())