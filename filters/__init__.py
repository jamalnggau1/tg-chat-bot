from aiogram import Dispatcher

from .is_admin import AdminFilter
from .is_chatting import ChattingFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(ChattingFilter)


__all__ = [
    "setup",
]
