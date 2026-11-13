from aiogram import Bot, Dispatcher
from data.config import config
from .handlers import router as handlers_router

bot = Bot(token=config.TELEGRAM_BOT_TOKEN.get_secret_value())
dp = Dispatcher()
dp.include_router(handlers_router)

async def start_bot():
    await dp.start_polling(bot)
    

async def stop_bot():
    await bot.session.close()