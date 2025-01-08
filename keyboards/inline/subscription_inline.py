from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

check_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Obuna bo'lish", url='https://t.me/abruis_code')
        ],
        [
            InlineKeyboardButton(text="🔄 Obunani tekshirish", callback_data="check_subs")
        ]
    ]
)

ha_yoq = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("✅ Ha", callback_data='ha'),
            InlineKeyboardButton("🚫 Yoq", callback_data='yoq')
        ]
    ]
)

ha_yoq_taklif = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("✅ Ha", callback_data='hataklif'),
            InlineKeyboardButton("🚫 Yoq", callback_data='yoqtaklif')
        ]
    ]
)

ha_yoq_taklif_tasqid = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton("✅ Ha", callback_data='hatakliftasdiq'),
            InlineKeyboardButton("🚫 Yoq", callback_data='yoqtakliftasdiq')
        ]
    ]
)