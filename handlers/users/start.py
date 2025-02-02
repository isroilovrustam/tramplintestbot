import requests
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import CHANNELS, API
from keyboards.inline.subscription_inline import check_button
from loader import dp
from utils.misc import subscription
from keyboards.default.start_button import start_btn, start_btnn

from html import escape


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user_id = message.from_user.id

    # Foydalanuvchi holatini aniqlash (API yoki ma'lumotlar bazasi orqali)
    response = requests.get(f"{API}/users/detail/{user_id}")
    user_full_name = escape(message.from_user.full_name)
    if response.status_code == 404:
        await message.answer(f"Salom, {user_full_name}!", reply_markup=start_btn)

    else:
        await message.answer(f"Salom, {user_full_name}!", reply_markup=start_btnn)


@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = str()
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        if status:
            await call.message.delete()
            result += (f"Yaxshi, {call.from_user.full_name} foydalanishingiz mumkin👇🏻")
            await call.message.answer(result, disable_web_page_preview=True)  # reply_markup=start_btn)
        else:
            await call.message.delete()
            result += (
                f"🚫Obuna bo'lmadingiz, qayta urinib ko'ring\n\n♻️Kanalga obuna bo'lib \"🔄 Obunani tekshirish\" ni bosing")
            await call.message.answer(result, disable_web_page_preview=True, reply_markup=check_button)
