import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from zoneinfo import ZoneInfo
from planner.tasks import task_morning, task_posting_statistic

from data.config import config

log = logging.getLogger(__name__)

class Planner:
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone=ZoneInfo(config.TIME_ZONE.get_secret_value()))
        self._register_tasks()

    def _register_tasks(self):

        self.scheduler.add_job(
            task_morning,
            trigger="cron",
            hour=16,
            minute=16,
            id="morning",
            name="morning task",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=3600
        )

        self.scheduler.add_job(
            task_posting_statistic,
            trigger="cron",
            hour=16,
            minute=16,
            id="statistic",
            name="statistic task",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=3600
        )

        log.debug("Planner tasks registered")

    def start(self):
        if not self.scheduler.running:
            self.scheduler.start()
            log.debug("Planner started")

    def stop(self):
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            log.debug("Planner stopped")