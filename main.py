import uvicorn
import asyncio
from contextlib import asynccontextmanager

from bot.bot import bot, dp, start_bot, stop_bot

from api.server import Server
from logger import configure_logger

configure_logger()
log = logging.getLogger(__name__)
log.debug("application started")

@asynccontextmanager
async def lifespan(app: FastAPI):

    # Запускаем Telegram-бота в фоне
    bot_task = asyncio.create_task(
        dp.start_polling(
            bot,
            handle_signals=False,
            close_bot_session=False,
            tasks_shutdown_timeout=30
        )
    )

    yield

    # Корректно останавливаем бота
    await dp.stop_polling()

    await bot_task

    await bot.session.close()


server = Server(lifespan=lifespan) 
