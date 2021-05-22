import asyncio
from datetime import datetime

from aiogram.types import Message
from aiogram.utils.exceptions import MessageToReplyNotFound

from data import texts
from keyboards import default, inline
from loader import bot, dp
from utils.db import db
from utils.misc import chat, spam_checker


@dp.edited_message_handler(state="*", content_types="any")
async def edited_message_handler(message: Message):
    try:
        partner_id = await db.user_data(message.from_user.id, "partner_id")
        await bot.edit_message_text(message.text, partner_id, message.message_id + 1)
    except:
        pass


async def process_lang_invalid(message: Message):
    return await message.reply(
        "<i>Выберите язык из предложенных ниже.\n"
        "Choose your language from the keyboard.</i>",
        reply_markup=inline.lang_btn,
    )


async def process_gender_invalid(message: Message):
    language = await db.execute_one_query(
        f'SELECT language FROM main WHERE user_id = "{message.from_user.id}"',
    )
    return await message.reply(
        "<i>Выберите пол из предложенных ниже.\n"
        "Choose your gender from the keyboard.</i>",
        reply_markup=await inline.gender_btn(language),
    )


async def not_chat_message_handler(message):
    return


async def chat_message_handler(message: Message):
    user_id = message.from_user.id
    partner_language, partner_id, language = await db.user_data(
        message.from_user.id,
        "partner_language",
        "partner_id",
        "language",
    )
    await asyncio.gather(spam_checker, message)
    print(datetime.now())
    try:
        if message.reply_to_message:
            msgid = (
                message.reply_to_message.message_id + 1
                if message.reply_to_message.from_user.id == user_id
                else message.reply_to_message.message_id - 1
            )
            if message.text:
                await bot.send_message(
                    partner_id, message.text, reply_to_message_id=msgid,
                )
            else:
                await bot.copy_message(
                    partner_id,
                    user_id,
                    message.message_id,
                    caption=message.caption,
                    reply_to_message_id=msgid,
                )
        else:
            if message.text:
                await bot.send_message(partner_id, message.text)
            else:
                await bot.copy_message(
                    partner_id,
                    user_id,
                    message.message_id,
                    caption=message.caption,
                )
    except MessageToReplyNotFound:
        if message.text:
            await bot.send_message(partner_id, message.text)
        else:
            await bot.copy_message(
                partner_id, user_id, message.message_id, caption=message.caption,
            )
    except:
        await db.disconnect(user_id, partner_id)
        await message.answer(
            f"<i>{texts.stop_chat[language][1]}</i>",
            reply_markup=await default.start_btn(language),
        )
        try:
            await bot.send_message(
                partner_id,
                f"<i>{texts.stop_chat[partner_language][1]}</i>",
                reply_markup=await default.start_btn(partner_language),
            )
            await bot.send_message(
                partner_id,
                f"<i>{texts.complain[partner_language]}</i>",
                reply_markup=await inline.complain_wth_rate_btn(
                    user_id, partner_language,
                ),
            )
        except:
            pass


async def another_message_handler(message: Message):
    language, isSearching, isSearchingByGender = await db.user_data(
        message.from_user.id, "language", "isSearching", "isSearchingByGender",
    )
    if (
        isSearching == "Y"
        or isSearchingByGender == "Y"
        and message.text in ["❌ Завершить поиск", "❌ End search"]
    ):
        await message.answer(
            f"<i>{texts.stop_search[language][0]}</i>",
            reply_markup=await default.start_btn(language),
        )
        await db.stop_search(message.from_user.id)
    elif message.text in ["✅ Поиск", "✅ Search"]:
        await chat.search(message)
    elif message.text in ["👩‍🦱 Поиск Ж", "👩‍🦱 Chat F"]:
        await chat.search_by_gender(message, sex="F")
    elif message.text in ["👨‍🦱 Поиск М", "👨‍🦱 Chat M"]:
        await chat.search_by_gender(message, sex="M")


__all__ = [
    "another_message_handler",
    "chat_message_handler",
    "edited_message_handler",
    "not_chat_message_handler",
    "process_gender_invalid",
    "process_lang_invalid",
]
