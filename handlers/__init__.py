from aiogram import Dispatcher

from states import Form

from . import callbacks, commands, messages


def setup(dp: Dispatcher):
    dp.register_message_handler(commands.start_command_handler, commands=["start"])
    dp.register_message_handler(
        commands.msgall_command_handler, commands=["msgall"], is_super_admin=True,
    )
    dp.register_message_handler(
        commands.info_command_handler, commands=["info"], is_super_admin=True,
    )
    dp.register_message_handler(
        commands.ban_command_handler, commands=["ban"], is_super_admin=True,
    )
    dp.register_message_handler(
        commands.unban_command_handler, commands=["unban"], is_super_admin=True,
    )
    dp.register_message_handler(
        commands.stats_command_handler, commands=["stats"], is_super_admin=True,
    )
    dp.register_message_handler(
        commands.sharelink_command_handler, commands=["sharelink"],
    )
    dp.register_message_handler(commands.next_command_handler, commands=["next"])
    dp.register_message_handler(commands.search_command_handler, commands=["search"])
    dp.register_message_handler(commands.stop_command_handler, commands=["stop"])
    dp.register_callback_query_handler(
        callbacks.set_user_gender, state=Form.GENDER, text=["M", "F"],
    )
    dp.register_callback_query_handler(
        callbacks.set_user_lang, state=Form.LANG, text=["en", "ru"],
    )
    dp.register_callback_query_handler(
        callbacks.report_handler, text_startswith="report",
    )
    dp.register_callback_query_handler(
        callbacks.report_reason_handler,
        text_startswith=[
            "Advertising",
            "Selling",
            "Child pornography",
            "Insult",
            "Other",
        ],
    )
    dp.register_callback_query_handler(
        callbacks.feedback_handler, text_startswith=["👍", "👎"],
    )
    dp.register_callback_query_handler(callbacks.ban_handler, text_startswith="ban")
    dp.register_message_handler(messages.process_lang_invalid, state=Form.LANG)
    dp.register_message_handler(messages.process_gender_invalid, state=Form.GENDER)
    dp.register_message_handler(
        messages.not_chat_message_handler,
        text=[
            "❌ Завершить поиск",
            "❌ End search",
            "✅ Поиск",
            "✅ Search",
            "👩‍🦱 Поиск Ж",
            "👩‍🦱 Chat F",
            "👨‍🦱 Поиск М",
            "👨‍🦱 Chat M",
        ],
        is_chatting=True,
    )
    dp.register_message_handler(
        messages.chat_message_handler, content_types="any", is_chatting=True,
    )
    dp.register_message_handler(messages.another_message_handler)
    dp.register_edited_message_handler(messages.edited_message_handler)


__all__ = [
    "setup",
]
