from aiogram.dispatcher.filters.state import StatesGroup, State


class RegisterState(StatesGroup):
    name = State()
    phone = State()


class TaklifState(StatesGroup):
    username = State()
    taklif = State()


class TestState(StatesGroup):
    question = State()  # Hozirgi savolni ko'rsatish
    answer = State()  # Foydalanuvchidan javob olish
