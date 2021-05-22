from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from utils.db import db


class ChattingFilter(BoundFilter):
    key = "is_chatting"

    def __init__(self, is_chatting):
        self.is_chatting = is_chatting

    async def check(self, message: types.Message, *args):
        return await db.is_chatting(message.from_user.id)


__all__ = [
    "ChattingFilter",
]
