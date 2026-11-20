from sqlalchemy import select, update, delete 
from sqlalchemy.ext.asyncio import AsyncSession
from .models import SnapshotHistory, CurrentSnapshot

class SnapshotHistoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, data: dict[str, Any]) -> SnapshotHistory:
        snapshot = SnapshotHistory(data=data)

        self.session.add(snapshot)
        await self.session.commit()
        await self.session.refresh(snapshot)

        return snapshot

    async def update(self, snapshot_id: int, data: dict[str, Any],) -> bool:
        query = (
            update(SnapshotHistory)
            .where(SnapshotHistory.id == snapshot_id)
            .values(data=data)
        )

        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0

    async def delete(self, snapshot_id: int) -> bool:
        query = delete(SnapshotHistory).where(
            SnapshotHistory.id == snapshot_id
        )

        result = await self.session.execute(query)
        await self.session.commit()

        return result.rowcount > 0


class CurrentSnapshotRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def insert(self, name: str, value: int | None) -> CurrentSnapshot:
        snapshot = CurrentSnapshot(
            name=name,
            value=value,
        )

        self.session.add(snapshot)
        await self.session.commit()
        await self.session.refresh(snapshot)

        return snapshot

    async def update(self, name: str, value: int | None,) -> bool:
        query = (
            update(CurrentSnapshot)
            .where(CurrentSnapshot.name == name)
            .values(value=value)
        )

        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0

    async def delete(self, name: str) -> bool:
        query = delete(CurrentSnapshot).where(
            CurrentSnapshot.name == name
        )

        result = await self.session.execute(query)
        await self.session.commit()

        return result.rowcount > 0