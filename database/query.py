from sqlalchemy import select, update, delete 
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from .models import SnapshotHistory, CurrentSnapshot
from typing import Any

from logging import getLogger

log = getLogger(__name__)

class SnapshotHistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, data: dict[str, Any]) -> SnapshotHistory:
        log.info("ADD SNAPSHOT TO TABLE SNAPSHOT_HISTORY")
        snapshot = SnapshotHistory(data=data)
        self.session.add(snapshot)
        await self.session.commit()
        log.info("CHANGES COMMITED")
        await self.session.refresh(snapshot)

        return snapshot

    async def delete(self, snapshot_id: int) -> bool:
        log.info("DELETE SNAPSHOT FROM TABLE SNAPSHOT_HISTORY")
        query = delete(SnapshotHistory).where(SnapshotHistory.id == snapshot_id)
        result = await self.session.execute(query)
        await self.session.commit()
        log.info("CHANGES COMMITED")
        return result.rowcount > 0

class CurrentSnapshotRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert(self, name: str, value: int | None) -> CurrentSnapshot:
        query = insert(CurrentSnapshot).values(name=name,value=value)

        query = query.on_conflict_do_update(
            index_elements=[CurrentSnapshot.name],
            set_={
                "value": query.excluded.value,
            },
        ).returning(CurrentSnapshot)

        result = await self.session.execute(query)
        await self.session.commit()
        log.info("CHANGES COMMITED")
        return result.scalar_one()

    async def delete(self, name: str) -> bool:
        query = delete(CurrentSnapshot).where(CurrentSnapshot.name == name)
        result = await self.session.execute(query)
        await self.session.commit()
        log.info("CHANGES COMMITED")        
        return result.rowcount > 0

    async def get_all(self) -> dict[str, int | None]:
        query = select(CurrentSnapshot.name, CurrentSnapshot.value)
        result = await self.session.execute(query)
        return dict(result.all())