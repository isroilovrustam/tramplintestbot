from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# "Start" tugmalari uchun markup
start_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📋 TEST ISHLASH")  # Test tugmasi
        ],
        [
            KeyboardButton(text="👤 Profilim"),  # Profil tugmasi
            KeyboardButton(text="📝 Taklif qoldirish")  # Shikoyat qilish tugmasi
        ]
    ],
    resize_keyboard=True,  # Tugmalarni mos ravishda kichraytirish
)

test_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="A"),
            KeyboardButton(text="B"),
            KeyboardButton(text="C"),
            KeyboardButton(text="D"),
        ]
    ],
    resize_keyboard = True,  # Tugmalarni mos ravishda kichraytirish
)
