from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import GROUP_ID
from loader import dp, bot
from keyboards.inline.subscription_inline import ha_yoq_taklif, ha_yoq_taklif_tasqid
from states.profile_state import TaklifState
from keyboards.default.start_button import start_btn


@dp.message_handler(text="📝 Taklif qoldirish")
async def enter_test(message: types.Message):
    await message.answer(f"Salom {message.from_user.full_name} Qanday taklifingiz bor ⁉️",
                         reply_markup=ha_yoq_taklif)


@dp.callback_query_handler(text='yoqtaklif')
async def hsa(call: types.CallbackQuery):
    await call.message.answer("Taklif yuborish bekor qilindi!")
    await call.message.delete()


@dp.callback_query_handler(text='hataklif')
async def hsa(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Marhamat taklifingizni yozishingiz mumkin!", reply_markup=types.ReplyKeyboardRemove())
    await TaklifState.taklif.set()


@dp.message_handler(state=TaklifState.taklif)
async def answer_fullname(message: types.Message, state: FSMContext):
    taklif = message.text

    await state.update_data(
        {"username": message.from_user.username}
    )

    await state.update_data(
        {"taklif": taklif}
    )

    # Ma`lumotlarni qayta o'qiymiz
    data = await state.get_data()
    username = data.get("username")
    taklif = data.get("taklif")

    msg = f"Taklif:\n\n"
    msg += f"👨‍💼 Username - {username}\n"
    msg += f"📝 Taklifingiz - {taklif}\n"
    msg += "‼️ Barcha ma'lumotlar to'g'rimi ‼️"

    await message.answer(msg, reply_markup=ha_yoq_taklif_tasqid)


@dp.callback_query_handler(state=TaklifState, text='hatakliftasdiq')
async def submit_data(call: types.CallbackQuery, state: FSMContext):
    # Ma`lumotlarni qayta o'qiymiz
    data = await state.get_data()
    username = data.get("username")
    taklif = data.get("taklif")

    msg = f"Taklif:\n\n"
    msg += f"👨‍💼 Username - {username}\n"
    msg += f"📝 Taklifingiz - {taklif}\n"

    # Ma'lumotlarni guruhga yuborish
    await bot.send_message(GROUP_ID, msg)

    await call.message.delete()
    await call.message.answer("✅ Ma'lumotlaringiz yuborildi!!!", reply_markup=start_btn)
    await state.finish()


@dp.callback_query_handler(state=TaklifState, text='yoqtakliftasdiq')
async def hsa(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("🚫 Ma'lumotingiz yuborilmadi!!!", reply_markup=start_btn)
    await call.message.delete()
    await state.finish()
