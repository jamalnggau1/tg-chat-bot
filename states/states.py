from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
    LANG = State()
    GENDER = State()
    PARTNER_GENDER = State()


__all__ = [
    "Form",
]
