from aiogram import Bot, Dispatcher
from config import Config

bot = Bot(token=Config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

async def start_bot():
    await dp.start_polling(bot)

async def stop_bot():
    await bot.session.close()