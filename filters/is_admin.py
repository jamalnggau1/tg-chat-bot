from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import ADMINS


class AdminFilter(BoundFilter):
    key = "is_super_admin"

    def __init__(self, is_super_admin):
        self.is_super_admin = is_super_admin

    async def check(self, message: types.Message, *args):
        return str(message.from_user.id) in ADMINS


__all__ = [
    "AdminFilter",
]
