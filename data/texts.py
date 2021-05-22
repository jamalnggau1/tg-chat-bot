stop_chat = [
    [
        """
Вы завершили диалог 😞
Напишите /search чтобы найти следующего""",
        """
Ваш собеседник отключился 😞
Напишите /search чтобы найти следующего""",
    ],
    [
        """
You have finished the dialog 😞
Type /search to find the next one""",
        """
Your partner has finished the conversation 😞
Type /search to find the next one""",
    ],
]

unavailable_command = [
    "Эта команда недоступна в данный момент.",
    "This command is not available at the moment.",
]

user_banned = [
    "Мы ограничили вам пользование чатом.\nПричина: {}.\n\n"
    "Снова пользоваться чатом вы сможете {}",
    "We have restricted your use of the chat.\nReason: {}.\n\n"
    "You will be able to use the chat again on {}",
]
user_unbanned = [
    "Вы разбанены.\nНадеемся вы ознакомлены с правилами и больше не будете их нарушать",
    "You are unblocked.\nWe hope you are familiar with the rules and will not break them again",
]

start_menu = [
    """
Добро пожаловать в анонимный телеграм чат

Доступные команды:
/next - Следующий собеседник
/search - Поиск собеседника
/stop - Закончить диалог
/sharelink - Отправить ссылку на ваш Telegram аккаунт

Отправьте мне текст, ссылки, гифки, стикеры, фотографии,
видео или голосовые сообщения, и я их анонимно
перешлю вашему собеседнику.""",
    """
Glad to see you in anonymous telegram chat

Available commands:
/next - Next partner
/search - Find a partner
/stop - End the dialog
/sharelink - Send a link to your Telegram Account

Send me text, links, GIFs, stickers, photos,
videos, or voice messages, and I
will forward them anonymously to your partner""",
]

sharelink = [
    [
        "У вас нет собеседника.",
        "Ваша ссылка отправлена собеседнику.",
        "Вот ссылка на мой телеграм-аккаунт.",
        "Отправлено командой",
    ],
    [
        "You don't have a partner.",
        "Your link has been sent to a partner.",
        "Here is the link to my telegram account.",
        "Sent with",
    ],
]
complain = [
    "Вы можете оценить вашего собеседника.Это поможет находить вам подходящих собеседников",
    "You can rate your partner.This will help you find the right people to talk to",
]
not_partner = ["У вас нет собеседника.", "You don't have a partner."]
already_have_partner = [
    "У вас уже есть собеседник.\n/next - найти нового",
    "You already have a partner.\n/next - next partner",
]
already_searching = [
    "Вы уже в поиске.\n/stop - остановить поиск",
    "You already have a partner.\n/stop - stop search",
]
stop_search = [
    [
        """
Вы завершили поиск 😞
Напишите /search чтобы найти следующего""",
    ],
    [
        """
You have finished the search 😞
Type /search to find the next one""",
    ],
]
female_search = [
    [
        """
Собеседник найден 🐵
/next — искать нового собеседника
/stop — закончить диалог""",
        "Ищем девушку...",
    ],
    [
        """
The partner is found 🐵
/next - next partner
/stop - End the dialog""",
        "Searching female...",
    ],
]
male_search = [
    [
        """
Собеседник найден 🐵
/next — искать нового собеседника
/stop — закончить диалог""",
        "Ищем парня...",
    ],
    [
        """
The partner is found 🐵
/next - next partner
/stop - End the dialog""",
        "Searching male...",
    ],
]
search = [
    [
        """
Собеседник найден 🐵
/next — искать нового собеседника
/stop — закончить диалог""",
        "Поиск...",
    ],
    [
        """
The partner is found 🐵
/next - next partner
/stop - End the dialog""",
        "Searching...",
    ],
]

reasons = [
    [
        "Распространение рекламы или скам материалов",
        "Продажа",
        "Распространение детской порнографии",
        "Оскорбление собеседника или грубое поведение",
        "Компромитирующие либо другие непристойные действия",
    ],
    [
        "Distribution of advertisements or scam materials",
        "Sale",
        "Distribution of child pornography",
        "Insulting the interlocutor or rude behavior",
        "Сompromising or other actions",
    ],
]
language_key = {
    "ru": [0, "✅ Язык успешно выбран", "Выберите ваш пол"],
    "en": [1, "✅ Language selected successfully", "Choose your gender"],
}


__all__ = [
    "already_have_partner",
    "already_searching",
    "complain",
    "female_search",
    "language_key",
    "male_search",
    "not_partner",
    "reasons",
    "search",
    "sharelink",
    "start_menu",
    "stop_chat",
    "stop_search",
    "unavailable_command",
    "user_banned",
    "user_unbanned",
]
