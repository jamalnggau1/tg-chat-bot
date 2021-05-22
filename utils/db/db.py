import asyncio
import datetime

from . import db_api


db_api = db_api.DB()


async def is_registered(user_id):
    if await user_data(user_id) is None:
        return False
    return True


async def update(query):
    await db_api.execute_query(query)


async def select(query):
    return await db_api.execute_one_query(query)


async def is_banned(user_id):
    if (
        await db_api.execute_one_query(
            f'SELECT * FROM UsersInBan WHERE id = "{user_id}"',
        )
        is None
    ):
        return False
    return True


async def is_chatting(user_id):
    if (
        await db_api.execute_one_query(
            f'SELECT isChatting FROM main WHERE user_id = "{user_id}"',
        )
        == "Y"
    ):
        return True
    return False


async def disconnect(user_id, partner_id):
    await db_api.execute_query(
        f'UPDATE main SET isChatting = "N", isChattingByGender = "N" WHERE user_id = "{user_id}"',
    )
    await db_api.execute_query(
        f'UPDATE main SET isChatting = "N", isChattingByGender = "N" WHERE user_id = "{partner_id}"',
    )


async def ban_user(user_id, reason, date):
    await db_api.execute_query(
        f'INSERT INTO UsersInBan VALUES ("{user_id}", "{reason}", "{date}" )',
    )


async def unban_user(user_id):
    await db_api.execute_query(f'DELETE FROM UsersInBan WHERE id = "{user_id}"')


async def user_data(user_id, *args):
    values = ""
    if args == ():
        return await db_api.execute_one_query(
            f'SELECT * FROM main WHERE user_id = "{user_id}"',
        )
    for value in args:
        values += value + ","
    return await db_api.execute_one_query(
        f'SELECT {values[:-1]} FROM main WHERE user_id = "{user_id}"',
    )


async def update_gender(user_id, gender):
    await db_api.execute_query(
        f'UPDATE main SET gender = "{gender}" WHERE user_id = "{user_id}"',
    )


async def update_language(user_id, language):
    key = {"ru": 0, "en": 1}
    await db_api.execute_query(
        f'UPDATE main SET language = "{key[language]}" WHERE user_id = "{user_id}"',
    )


async def update_rating(user_id, rating):
    await db_api.execute_query(
        f'UPDATE main SET rating = rating + "{rating}" WHERE user_id = "{user_id}"',
    )


async def register_user(user_id):
    await db_api.execute_query(
        "INSERT INTO main "
        f'VALUES ("{user_id}","0", "N","N", "N", "None", "None","",'
        '"0", "0","0","0", "N")',
    )


async def select_users():
    return await db_api.execute_all_query("SELECT * FROM main")


async def delete_user(user_id):
    await db_api.execute_query(f'DELETE FROM main WHERE user_id = "{user_id}"')


async def stop_search(user_id):
    await db_api.execute_query(
        f'UPDATE main SET isSearching = "N", isSearchingByGender = "N" WHERE user_id = "{user_id}"',
    )


async def delete_users(user_id):
    await db_api.execute_query(f'DELETE FROM main WHERE user_id = "{user_id}"')


async def stats():
    args = [
        'SELECT user_id FROM main WHERE IsChatting = "Y" ',
        'SELECT user_id FROM main WHERE IsSearching = "Y" ',
        'SELECT user_id FROM main WHERE IsSearchingByGender = "Y" ',
        'SELECT user_id FROM main WHERE gender = "M" ',
        'SELECT user_id FROM main WHERE gender = "F" ',
        'SELECT user_id FROM main WHERE (IsSearching = "Y" OR IsSearchingByGender = "Y") AND gender = "M"',
        'SELECT user_id FROM main WHERE (IsSearching = "Y" OR IsSearchingByGender = "Y") AND gender = "F"',
    ]
    tasks = []
    for arg in args:
        task = db_api.execute_all_query(arg)
        tasks.append(task)
    (
        chatting,
        serching,
        gender_serching,
        male,
        female,
        male_serching,
        female_serching,
    ) = await asyncio.gather(*tasks)

    return f"""
Активных чатов: {int(len(chatting) / 2)}
Человек в поиске: {len(serching)}
Человек в поиске по полу: {len(gender_serching)}
В поиске парней: {len(male_serching)}
В поиске девушек: {len(female_serching)}
Зарегистрировано девушек: {len(female)}
Зарегистрировано парней: {len(male)}
                            """


async def check_ban(user_id):
    date, reason = await db_api.execute_one_query(
        f'SELECT date, reason FROM UsersInBan WHERE id = "{user_id}"',
    )
    date_time_obj = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
    if date_time_obj > datetime.datetime.now():
        return date, reason
    else:
        await unban_user(user_id)
        return False, None


__all__ = [
    "ban_user",
    "check_ban",
    "db_api",
    "delete_user",
    "delete_users",
    "disconnect",
    "is_banned",
    "is_chatting",
    "is_registered",
    "register_user",
    "select",
    "select_users",
    "stats",
    "stop_search",
    "unban_user",
    "update",
    "update_gender",
    "update_language",
    "update_rating",
    "user_data",
]
