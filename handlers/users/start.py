from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import CHANNELS
from keyboards.inline.subscription_inline import check_button
from loader import dp
from utils.misc import subscription
from keyboards.default.start_button import start_btn


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f"Salom, {message.from_user.full_name}!", reply_markup=start_btn)


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
