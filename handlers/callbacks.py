from datetime import datetime, timedelta

from aiogram.dispatcher.storage import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from data import texts
from data.config import BD_ANON_ID
from keyboards import default, inline
from loader import bot
from states import Form
from utils.db import db
from utils.misc.checker import msgcont


async def set_user_lang(query: CallbackQuery, state: FSMContext):
    await db.update_language(query.from_user.id, query.data)
    await query.message.edit_text(
        f"{texts.language_key[query.data][1]}\n{texts.language_key[query.data][2]}",
        reply_markup=await inline.gender_btn(texts.language_key[query.data][0]),
    )
    await Form.next()


async def set_user_gender(query: CallbackQuery, state: FSMContext):
    text = ["Ваш пол успешно выбран.", "Your gender was successfully selected."]
    language = await db.user_data(query.from_user.id, "language")
    await db.update_gender(query.from_user.id, query.data)
    await query.message.edit_text(f"<i>{text[language]}</i>")
    await query.message.answer(
        f"<i>{texts.start_menu[language]}</i>",
        reply_markup=await default.start_btn(language),
    )
    await state.finish()


async def report_handler(query: CallbackQuery):
    txt = ["Выберите причину:", "Choose a reason:"]
    language = await db.user_data(query.from_user.id, "language")
    _, user_id = query.data.split("<i>")
    await query.message.edit_text(
        f"<i>{txt[language]}</i>",
        reply_markup=await inline.complain1_btn(user_id, language),
    )


async def report_reason_handler(query: CallbackQuery, state: FSMContext):
    txt = ["Спасибо за отзыв!", "Thank you for your feedback!"]
    language = await db.user_data(query.from_user.id, "language")
    reason, user_id = query.data.split("<i>")
    await query.message.edit_text(f"<i>{txt[language]}</i>")
    await db.update_rating(user_id, -1)
    msg_ids = ""
    for msgid in msgcont[int(user_id)]:
        msg = await bot.copy_message(BD_ANON_ID, user_id, msgid)
        msg_ids += str(msg.message_id) + "-"
    await bot.send_message(
        BD_ANON_ID,
        f"Report\nReason: {reason}\nInfo:\n[{user_id}](tg://user?id={user_id})",
        reply_markup=await inline.ban_btn(user_id, reason, msg_ids),
    )


async def feedback_handler(query: CallbackQuery):
    keys = {"👎": -1, "👎": 1}
    txt = ["Спасибо за отзыв!", "Thank you for your feedback!"]
    language = await db.user_data(query.from_user.id, "language")
    key, user_id = query.data.split("<i>")
    await db.update_rating(user_id, keys[key])
    await query.message.edit_text(f"<i>{txt[language]}</i>")


async def ban_handler(query: CallbackQuery):
    language = await db.user_data(query.from_user.id, "language")
    _, reason, day, user_id, ids = query.data.split("<i>")
    days = timedelta(int(day))
    now = datetime.now()
    date = now + days
    x = {"Selling": 0, "Advertising": 1, "CP": 2, "Insult": 3, "Violence": 4}

    if await db.is_chatting(user_id):
        (
            partner_id,
            partner_language,
        ) = await db.user_data(user_id, "partner_id", "partner_language")
        await db.disconnect(user_id, partner_id)
        await bot.send_message(
            partner_id,
            f"<i>{texts.stop_chat[partner_language][1]}</i>",
            reply_markup=await default.start_btn(partner_language),
        )
        await bot.send_message(
            user_id,
            f"<i>{texts.stop_chat[language][1]}</i>",
            reply_markup=ReplyKeyboardRemove(),
        )

    if not await db.is_banned(user_id):
        await db.ban_user(user_id, reason, date)
    await query.message.edit_text(
        f"[banned](tg://user?id={user_id})_ for {day} days, reason: {texts.reasons[language][x[reason]]}._",
        parse_mode="Markdown",
    )
    for id in ids.split("-")[:-1]:
        await bot.delete_message(BD_ANON_ID, int(id))
    await bot.send_message(
        user_id,
        f"<i>{texts.user_banned[language]}</i>".format(
            texts.reasons[language][x[reason]], str(date)[:16],
        ),
    )


__all__ = [
    "ban_handler",
    "feedback_handler",
    "report_handler",
    "report_reason_handler",
    "set_user_gender",
    "set_user_lang",
]
