from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from .database import Database

class DatabaseConnection:
    def __init__(self, database: Database):
        self.database = Database()
        self.session_factory = async_sessionmaker(
            bind=self.database.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    async def get_session(self):
        async with self.session_factory() as session:
            yield session