import logging
import asyncio

from bot.bot import bot
from data.config import config
admin_id = int(config.TELEGRAM_ADMIN_ID.get_secret_value())

log = logging.getLogger(__name__)

async def task_morning():
    log.debug("task morning start")
    try:
        await bot.send_message(
            chat_id=admin_id,
            text="task morning"
        )

        log.debug("task morning completed")
    except Exception:
        log.exception("morning error")

async def task_posting_statistic():
    log.debug("task statistic start")
    try:
        await bot.send_message(
            chat_id=admin_id,
            text="test_statistic"
        )
        log.debug("task statistic completed")
    except Exception:
        log.exception("statistic error")