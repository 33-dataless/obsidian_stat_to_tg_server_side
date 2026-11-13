import asyncio
import logging

from fastapi import FastAPI
from contextlib import asynccontextmanager

from bot.bot import bot, dp
from api.server import Server
from planner.planner import Planner

from logger import configure_logger

configure_logger()
log = logging.getLogger(__name__)
planner = Planner()

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("APPLICATION STARTING")
    planner.start()

    bot_task = asyncio.create_task(
        dp.start_polling(
            bot,
            handle_signals=False,
            close_bot_session=False,
            tasks_shutdown_timeout=30
        )
    )

    try:
        yield

    finally:
        log.info("APPLICATION STOPPING")
        planner.stop()
        if not bot_task.done():
            await dp.stop_polling()
        try:
            await bot_task
        finally:
            await bot.session.close()
        log.info("APPLICATION STOPPED")

server = Server(lifespan=lifespan)