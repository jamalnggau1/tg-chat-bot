from aiogram.types import Message
from aiogram.types.reply_keyboard import ReplyKeyboardRemove

from data import texts
from keyboards import default
from loader import bot
from utils.db import db


async def search_by_gender(message: Message, sex):
    user_id = message.from_user.id
    gender, rating, language = await db.user_data(
        message.from_user.id, "gender", "rating", "language",
    )
    sort = "ASC" if rating >= 0 else "DESC"
    text = texts.female_search if sex == "F" else texts.male_search
    await message.answer(
        f"<i>{text[language][1]}</i>",
        reply_markup=await default.exit_btn(language),
    )
    while True:
        partner = await db.select(
            f'SELECT * FROM main WHERE user_id != "{user_id}" AND (rating <= "{rating}"+10'
            f' AND rating >= "{rating}"-10) AND gender = "{sex}" AND (IsSearching = "Y" '
            f'OR (isSearchingByGender = "Y" AND partner_gender = "{gender}")) ORDER BY rating {sort}',
        )
        if partner is None:
            partner = await db.select(
                f'SELECT * FROM main WHERE user_id != "{user_id}" AND gender = "{sex}" AND (IsSearching = "Y" '
                f'OR (isSearchingByGender = "Y" AND partner_gender = "{gender}")) ORDER BY rating {sort}',
            )
            if partner is None:
                await db.update(
                    f'UPDATE main SET isSearchingByGender = "Y", partner_gender = "{sex}"  WHERE user_id = "{user_id}"',
                )
                return
        try:
            x = (
                'isChattingByGender = "Y"'
                if partner[3] == "Y"
                else 'isChattingByGender = "N"'
            )
            await db.update(
                f'UPDATE main SET isSearching = "N", isSearchingByGender = "N", isChatting = "Y", {x}, partner_id = "{user_id}",'
                f'partner_gender = "{gender}", partner_language = "{language}" WHERE user_id = "{partner[0]}"',
            )
            await db.update(
                'UPDATE main SET isSearching = "N", isSearchingByGender = "N", isChatting = "Y", isChattingByGender = "Y",'
                f'partner_id = "{partner[0]}", partner_gender = "{partner[5]}", partner_language = "{partner[8]}" WHERE user_id = "{user_id}"',
            )
            await bot.send_message(
                partner[0],
                f"<i>{text[partner[8]][0]}</i>",
                reply_markup=ReplyKeyboardRemove(),
            )
            await message.answer(
                f"<i>{text[language][0]}</i>",
                reply_markup=ReplyKeyboardRemove(),
            )

            return
        except:
            await db.update(
                'UPDATE main SET isSearchingByGender = "Y", isChatting = "N", isChattingByGender = "N",'
                f'partner_gender = "{sex}"  WHERE user_id = "{user_id}"',
            )
            await db.delete_user(partner[0])


async def search(message):
    user_id = message.from_user.id
    gender, rating, language = await db.user_data(
        message.from_user.id, "gender", "rating", "language",
    )
    sort = "ASC" if rating >= 0 else "DESC"
    text = texts.search
    await message.answer(
        f"<i>{text[language][1]}</i>",
        reply_markup=await default.exit_btn(language),
    )
    while True:
        partner = await db.select(
            f'SELECT * FROM main WHERE user_id != "{user_id}" AND '
            f'(rating <= "{rating}"+10 AND rating >= "{rating}"-10) AND (IsSearching = "Y" '
            f'OR (isSearchingByGender = "Y" AND partner_gender = "{gender}")) AND isChatting == "N" ORDER BY rating {sort}',
        )
        if partner is None:
            partner = await db.select(
                f'SELECT * FROM main WHERE user_id != "{user_id}" AND (IsSearching = "Y" OR'
                f'(isSearchingByGender = "Y" AND partner_gender = "{gender}")) ORDER BY rating {sort}',
            )
            if partner is None:
                await db.update(
                    f'UPDATE main SET isSearching = "Y" WHERE user_id = "{user_id}"',
                )
                return
        try:
            x = (
                'isChattingByGender = "Y"'
                if partner[3] == "Y"
                else 'isChattingByGender = "N"'
            )
            await db.update(
                f'UPDATE main SET isSearching = "N", isSearchingByGender = "N", isChatting = "Y", {x},'
                f'partner_id = "{user_id}", partner_gender = "{gender}", partner_language = "{language}" WHERE user_id = "{partner[0]}"',
            )
            await db.update(
                f'UPDATE main SET isSearching = "N", isSearchingByGender = "N", isChatting = "Y", partner_id = "{partner[0]}",'
                f'partner_gender = "{partner[5]}", partner_language = "{partner[8]}" WHERE user_id = "{user_id}"',
            )
            await bot.send_message(
                partner[0],
                f"<i>{text[partner[8]][0]}</i>",
                reply_markup=ReplyKeyboardRemove(),
            )
            await message.answer(
                f"<i>{text[language][0]}</i>",
                reply_markup=ReplyKeyboardRemove(),
            )
            return
        except:
            await db.update(
                f'UPDATE main SET isSearching = "Y", isChatting = "N", isChattingByGender = "N" WHERE user_id = "{user_id}"',
            )
            await db.delete_user(partner[0])

__all__ = [
    "search",
    "search_by_gender",
]
