from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


async def exit_btn(lang):
    s = ["❌ Завершить поиск", "❌ End search"]
    exit_btn1 = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    exit_btn1.row(KeyboardButton(text=f"{s[lang]}"))
    return exit_btn1


async def start_btn(lang):
    s = [
        [
            "✅ Поиск",
            "👨‍🦱 Поиск М",
            "👩‍🦱 Поиск Ж",
        ],
        ["✅ Search", "👨‍🦱 Chat M", "👩‍🦱 Chat F"],
    ]
    start_btn1 = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    start_btn1.row(KeyboardButton(text=f"{s[lang][0]}"))
    start_btn1.row(
        KeyboardButton(text=f"{s[lang][1]}"), KeyboardButton(text=f"{s[lang][2]}"),
    )
    return start_btn1


__all__ = [
    "exit_btn",
    "start_btn",
]
