from .bot import bot
from aiogram.types import Message, MessageEntity
from data.config import config

async def post(increased: int, decreased: int, all_chars: int):
    text = (
        "изменения в Obsidian\n\n"

        "добавлено новых символов: 🟩 " + str(increased) + "\n"
        "удалено символов: 🟥" + str(decreased) + "\n"
        "общее колво символов: 🫆" + str(all_chars) + "\n\n"

        "сделал фернандо агент"
    )

    await bot.send_message(chat_id=config.CHANNEL_ID.get_secret_value(), text=text)
