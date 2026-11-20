from data.models import Payload
from data.event import Event
from database.manager import db
from database.query import SnapshotHistoryRepository, CurrentSnapshotRepository
from statistic.snapshot_statistic import SnapshotStatistic
from bot.utils import post
import logging

log = logging.getLogger(__name__)

class Receiver:
    def __init__(self):
        pass

    async def process(self, payload: Payload):
        match payload.event:
            case Event.OBSIDIAN:
                await self._handle_obsidian(payload.snapshot)

            case Event.GITHUB:
                await self._handle_github(payload.snapshot)

            case Event.CHESS:
                await self._handle_chess(payload.snapshot)
        
    async def _handle_obsidian(self, snapshot: dict):
        log.info("OBSIDIAN HANDLED")
        async for session in db.get_session():
            history = SnapshotHistoryRepository(session)
            await history.insert(snapshot)

            current_snapshot_repository = CurrentSnapshotRepository(session)
            old_snapshot = await current_snapshot_repository.get_all()

            stat = SnapshotStatistic()
            new_snapshot = snapshot
            count = await stat.count_changes(new_snapshot=new_snapshot, old_snapshot=old_snapshot)
            await post(count[0], count[1], count[2])


            for key, value in snapshot.items():
                await current_snapshot_repository.upsert(key, value)

    def _handle_chess(self):
        pass

    def _handle_github(self):
        pass
