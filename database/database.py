import os 
import logging
from data.config import config 

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import DeclarativeBase

log = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

class Database:
    def __init__(self):
        log.info("DATABASE INITIATED")
        self.engine: AsyncEngine = create_async_engine(
            url = config.DATABASE_URL.get_secret_value(),
            # echo=True,
            pool_size=10,
            max_overflow=20
        )

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def dispose(self):
        await self.engine.dispose()