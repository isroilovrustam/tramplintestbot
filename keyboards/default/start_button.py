from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types.web_app_info import WebAppInfo
# "Start" tugmalari uchun markup
start_btnn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Test ishlash")  # Test tugmasi
        ],
        [
            KeyboardButton(text="👤 Profilim"),  # Profil tugmasi
            KeyboardButton(text="🌐 Test natijalar", web_app=WebAppInfo(url="https://abruis.uz/"))
        ],
        [
            KeyboardButton(text="📨 Taklif qoldirish")  # Shikoyat qilish tugmasi
        ]
    ],
    resize_keyboard=True,  # Tugmalarni mos ravishda kichraytirish
)
# "Start" tugmalari uchun markup
start_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📝 Test ishlash")  # Test tugmasi
        ],
        [
            KeyboardButton(text="📋 Ro'yxatdan o'tish"),  # Profil tugmasi
            KeyboardButton(text="🌐 Test natijalar", web_app=WebAppInfo(url="https://abruis.uz/"))
        ],
        [
            KeyboardButton(text="📨 Taklif qoldirish")  # Shikoyat qilish tugmasi
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
    resize_keyboard=True,  # Tugmalarni mos ravishda kichraytirish
)


contact_btn = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="☎️ Contact yuborish", request_contact=True)
        ]
    ],
    resize_keyboard=True
)