from aiogram import Dispatcher

from .registered import RegisteredMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(RegisteredMiddleware())


__all__ = [
    "setup",
]
