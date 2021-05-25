from aiogram import executor

import filters
import handlers
import middlewares
from utils.misc.set_bot_commands import set_default_commands
from utils.misc import logging
from loader import dp


async def on_startup(dispatcher):

    middlewares.setup(dispatcher)
    filters.setup(dispatcher)
    handlers.setup(dispatcher)

    await set_default_commands(dispatcher)


if __name__ == "__main__":

    executor.start_polling(dp, on_startup=on_startup)


__all__ = [
    "on_startup",
]
