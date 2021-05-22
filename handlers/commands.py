import asyncio
from datetime import datetime, timedelta

from aiogram.types import Message

from data import texts
from data.config import BD_ANON_ID
from keyboards import default, inline
from loader import bot
from states import Form
from utils.db import db
from utils.misc import chat


async def start_command_handler(message: Message):
    row = await db.user_data(message.from_user.id)
    if row[4] != "Y":
        await message.reply(
            "Выберите язык/Choose language ", reply_markup=inline.lang_btn,
        )
        await Form.LANG.set()
    else:
        await message.answer(
            texts.unavailable_command[row[8]],
        )


async def ban_command_handler(message: Message):

    user_id = message.text.split()[1]
    reason = message.text.split()[2]
    days = timedelta(int(message.text.split()[3]))
    now = datetime.datetime.now()
    date = now + days
    partner_id, isChatting, language, partner_language = await db.user_data(
        user_id, "partner_id", "isChatting", "language", "partner_language",
    )
    x = {"Selling": 0, "Advertising": 1, "CP": 2, "Insult": 3, "Violence": 4}
    if isChatting == "Y":
        await db.disconnect(user_id, partner_id)
        await bot.send_message(
            user_id,
            f"<i>{texts.stop_chat[language][1]}</i>",
            reply_markup=await default.start_btn(partner_language),
        )
        await bot.send_message(
            partner_id,
            f"<i>{texts.stop_chat[partner_language][1]}</i>",
            reply_markup=await default.start_btn(partner_language),
        )
    await bot.send_message(
        user_id,
        f"<i>{texts.user_banned[language]}</i>".format(
            texts.reasons[language][x[reason]], str(date)[:16],
        ),
    )

    if await db.is_banned(user_id) is None:
        await db.ban_user(user_id, texts.reasons[language][x[reason]], date)
        return await message.answer("Вы забанили пользователя")
    return await message.answer("Этот человек уже забанен")


async def info_command_handler(message: Message):
    partner_id = await db.user_data(message.from_user.id, "partner_id")
    await message.answer(
        "тихон лох соси писох",
    )
    await asyncio.sleep(6)
    await message.answer(
        f"\nInfo:\n[{partner_id}](tg://user?id={partner_id})", parse_mode="Markdown",
    )


async def unban_command_handler(message):
    await db.unban_user(message.text.split()[1])
    await message.answer("Вы разбанили пользователя")


async def msgall_command_handler(message: Message):
    user_ids = await db.select_users()
    ok, error = 0, 0
    for i in range(len(user_ids)):
        try:
            await bot.copy_message(
                user_ids[i][0], BD_ANON_ID, int(message.text.split()[1]),
            )
            ok += 1
        except:
            error += 1
    await message.answer(
        text=f"Всего: {len(user_ids)}\n\nУспешно: {ok}\n\nНеудачно: {error}",
    )


async def sharelink_command_handler(message: Message):
    isChatting, partner_language, partner_id, language = await db.user_data(
        message.from_user.id, "isChatting", "partner_language", "partner_id", "language",
    )
    if isChatting == "Y":
        await message.answer(
            f"<i>{texts.sharelink[language][1]}</i>",
        )
        await bot.send_message(
            partner_id,
            f"[{texts.sharelink[partner_language][2]}](tg://user?id={message.from_user.id})\n\n_{texts.sharelink[partner_language][3]} /sharelink_",
            parse_mode="Markdown",
        )
    else:
        await message.answer(
            f"<i>{texts.sharelink[language][0]}</i>",
        )


async def stats_command_handler(message: Message):
    await message.answer(await db.stats())


async def help_command_handler(message: Message):
    text = ("Список команд: ", "/start - Начать диалог", "/help - Получить справку")

    await message.answer("\n".join(text))


async def next_command_handler(message: Message):
    user_id = message.from_user.id
    (
        isChatting,
        isChattingByGender,
        isSearching,
        isSearchingByGender,
        partner_language,
        partner_id,
        partner_gender,
        language,
    ) = await db.user_data(
        message.from_user.id,
        "isChatting",
        "isChattingByGender",
        "isSearching",
        "isSearchingByGender",
        "partner_language",
        "partner_id",
        "partner_gender",
        "language",
    )
    if isChatting == "Y":
        await message.answer(
            f"<i>{texts.complain[language]}</i>",
            reply_markup=await inline.complain_wth_rate_btn(partner_id, language),
        )
        try:
            await db.disconnect(user_id, partner_id)
            await bot.send_message(
                partner_id,
                f"<i>{texts.stop_chat[partner_language][1]}</i>",
                reply_markup=await default.start_btn(partner_language),
            )
            await bot.send_message(
                partner_id,
                f"<i>{texts.complain[partner_language]}</i>",
                reply_markup=await default.complain_wth_rate_btn(
                    user_id, partner_language,
                ),
            )
        except:
            await db.delete_user(partner_id)
        if isChattingByGender == "Y":
            await chat.search_by_gender(message, partner_gender)
        else:
            await chat.search(message)
    elif isSearching == "Y" or isSearchingByGender == "Y":
        await message.answer(
            f"<i>{texts.already_searching[language]}</i>",
            reply_markup=await default.exit_btn(language),
        )
    else:
        await chat.search(message)


async def stop_command_handler(message: Message):
    user_id = message.from_user.id
    (
        isChatting,
        isSearching,
        isSearchingByGender,
        partner_language,
        partner_id,
        language,
    ) = await db.user_data(
        message.from_user.id,
        "isChatting",
        "isSearching",
        "isSearchingByGender",
        "partner_language",
        "partner_id",
        "language",
    )
    if isSearching == "Y" or isSearchingByGender == "Y":
        await message.answer(
            f"<i>{texts.stop_search[language][0]}</i>",
            reply_markup=await default.start_btn(language),
        )
        await db.stop_search(user_id)
    elif isChatting == "Y":
        await db.disconnect(user_id, partner_id)
        await message.answer(
            f"<i>{texts.stop_chat[language][0]}</i>",
            reply_markup=await default.start_btn(language),
        )
        await message.answer(
            f"<i>{texts.complain[language]}</i>",
            reply_markup=await inline.complain_wth_rate_btn(partner_id, language),
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
            await db.delete_user(partner_id)
    else:
        await message.answer(
            f"<i>{texts.not_partner[language]}</i>",
            reply_markup=await default.start_btn(language),
        )


async def search_command_handler(message: Message):
    message.from_user.id
    isChatting, isSearching, isSearchingByGender, language = await db.user_data(
        message.from_user.id,
        "isChatting",
        "isSearching",
        "isSearchingByGender",
        "language",
    )
    if isChatting == "Y":
        await message.answer(
            f"<i>{texts.already_have_partner[language]}</i>",
        )
    elif isSearching == "Y" or isSearchingByGender == "Y":
        await message.answer(
            f"<i>{texts.already_searching[language]}</i>",
            reply_markup=await default.exit_btn(language),
        )
    else:
        await chat.search(message)


__all__ = [
    "ban_command_handler",
    "help_command_handler",
    "info_command_handler",
    "msgall_command_handler",
    "next_command_handler",
    "search_command_handler",
    "sharelink_command_handler",
    "start_command_handler",
    "stats_command_handler",
    "stop_command_handler",
    "unban_command_handler",
]
