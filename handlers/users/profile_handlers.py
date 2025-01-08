from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import GROUP_ID
from loader import dp, db, bot
from states.profile_state import RegisterState


@dp.message_handler(text='👤 Profilim')
async def profile_handler(message: types.Message):
    user_id = message.from_user.id

    # Foydalanuvchini tekshirish
    user = db.select_user(user_id)  # Database sinfi orqali foydalanuvchi ma'lumotlarini olish
    if user:
        name = user[1]  # Ism
        username = user[2]  # Username
        phone = user[3]  # Telefon
        score = user[4]
        passed = user[5]
        response = f"👤 Profil ma'lumotlaringiz:\n\nIsm: {name}\nUsername: {username}\nTelefon: {phone}\nScore: {score}\nPassed: {passed}"
        await dp.bot.send_message(message.from_user.id, response)  # Xabar yuborish

    else:
        response = "Siz ro'yxatdan o'tmagan ekansiz. Iltimos, ro'yxatdan o'ting."
        await dp.bot.send_message(message.from_user.id, response)  # Xabar yuborish
        await message.answer("Ismingizni kiriting:")
        await RegisterState.name.set()


@dp.message_handler(state=RegisterState.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)

    await message.answer("Endi telefon raqamingizni yuboring:")
    await RegisterState.phone.set()


@dp.message_handler(state=RegisterState.phone)
async def get_phone(message: types.Message, state: FSMContext):
    phone = message.text
    await state.update_data(phone=phone)
    user_id = message.from_user.id
    username = message.from_user.username

    data = await state.get_data()
    name = data.get("name")
    phone = data.get("phone")

    # Ma'lumotlarni saqlash
    db.add_user(user_id, name, username, phone)

    await message.answer(
        "✅ Ro'yxatdan muvaffaqiyatli o'tdingiz!\nSizning ma'lumotlaringiz saqlandi.")
    group_message = f"Yangi foydalanuvchi ro'yxatdan o'tdi:\n\nIsm: {name}\nUsername: @{username}\nTelefon: {phone}"
    await bot.send_message(GROUP_ID, group_message)
    await state.finish()
