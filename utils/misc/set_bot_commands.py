from aiogram import types


async def set_default_commands(dp):

    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Перезапустить бота / Restart a bot"),
            types.BotCommand("next", "Следующий собеседник / Next partner"),
            types.BotCommand("search", "Начать поиск / Find a partner"),
            types.BotCommand("stop", "Завершить диалог / End the dialog"),
            types.BotCommand("sharelink", "Поделиться профилем / Send a link to your Telegram Account"),
        ],
    )


__all__ = [
    "set_default_commands",
]
