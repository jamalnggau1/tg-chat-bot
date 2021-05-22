from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data import texts
from utils.db import db


class RegisteredMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def on_process_message(self, message: types.Message, data):
        user = await db.is_registered(message.from_user.id)
        if not user:
            await db.register_user(message.from_user.id)
            if message.text != "/start":
                await message.reply("Нажмите /start")
                raise CancelHandler()
        if user and await db.is_banned(message.from_user.id):
            date, reason = await db.check_ban(message.from_user.id)
            await message.answer(
                f"<i>{texts.user_banned[await db.user_data(message.from_user.id, 'language')].format(reason, date[:16])}</i>",
            )
            raise CancelHandler()


__all__ = [
    "RegisteredMiddleware",
]
