from collections import Counter

from aiogram.types import Message

from data.config import ARCHIVE_ID, BD_ANON_ID
from keyboards import inline
from loader import bot


msgcont = {}
spam = {}


async def spam_checker(message: Message):
    global msgcont, spam
    try:
        if len(msgcont[message.from_user.id]) == 5:
            del msgcont[message.from_user.id][0]
        msgcont[message.from_user.id].append(message.message_id)
    except:
        msgcont[message.from_user.id] = [message.message_id]
    msgtype = message.text if message.text else message.content_type
    try:
        spam[message.from_user.id].append(msgtype)
    except:
        spam[message.from_user.id] = [msgtype]
    if len(spam[message.from_user.id]) == 10:
        if len(Counter(spam[message.from_user.id])) < 3:
            spam[message.from_user.id] == []
            x = await bot.copy_message(
                BD_ANON_ID,
                message.from_user.id,
                message.message_id,
                caption=f"spam\n[{message.from_user.first_name}](tg://user?id={message.from_user.id})",
                reply_markup=await inline.ban_btn(message.from_user.id, "Violence"),
                parse_mode="Markdown",
            )
        spam[message.from_user.id] = []
    if msgtype in ["photo", "video", "video_note", "document"]:
        await bot.copy_message(
            ARCHIVE_ID,
            message.from_user.id,
            message.message_id,
            caption=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})",
            parse_mode="Markdown",
        )


__all__ = [
    "msgcont",
    "spam",
    "spam_checker",
]
