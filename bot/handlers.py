from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from .admin_filter import AdminFilter
from data.config import config

router = Router()
admin_id = int(config.TELEGRAM_ADMIN_ID.get_secret_value())

@router.message(CommandStart(), AdminFilter(admin_id))
async def start(message: Message):
    await message.answer("bot 200")

