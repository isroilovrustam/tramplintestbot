import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentTypes

from data.config import GROUP_ID, API
from keyboards.default.start_button import start_btnn, contact_btn
from loader import dp, bot
from states.profile_state import RegisterState


@dp.message_handler(text='👤 Profilim')
async def profile_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        # Telegram ID asosida API orqali foydalanuvchi ma'lumotlarini olish
        response = requests.get(url=f"{API}/users/detail/{user_id}")
        response.raise_for_status()  # Agar xatolik bo'lsa, exception ko'taradi
        user = response.json()
        # print(user)

        if user:
            # API'dan qaytgan ma'lumotlarni qayta ishlash
            full_name = user.get("full_name", "Noma'lum")
            username = user.get("username", "Noma'lum")
            phone = user.get("phone", "Noma'lum")
            score = user.get("score", 0)
            passed = user.get("passed", 0)

            passed_status = "✅ Tabriklaymiz, siz o'tdingiz!" if int(passed) == 1 else "❌ Afsus, o'ta olmadingiz"

            # Javob xabari
            response_text = (
                f"👤 Sizning profil ma'lumotlaringiz:\n\n"
                f"🧑‍💼 Ism: {full_name}\n"
                f"🆔 Username: @{username}\n"
                f"📞 Telefon: {phone}\n"
                f"⭐ Sizning balingiz: {score}\n"
                f"❓ Natija: {passed_status}"
            )

        else:
            # Agar foydalanuvchi topilmasa
            response_text = (
                "⚠ Siz ro'yxatdan o'tmagan ekansiz.\n"
                "Iltimos, ma'lumotlaringizni kiritib, ro'yxatdan o'ting."
            )
            await message.answer("Ismingizni kiriting:")
            # await RegisterState.name.set()  # Foydalanuvchini ro'yxatdan o'tish jarayoniga o'tkazish

    except requests.RequestException as e:
        # Agar API so'rovda muammo bo'lsa
        response_text = (
            "⚠️ Siz ro'yxatdan o'tmagan ekansiz.\n"
            "Iltimos, ma'lumotlaringizni kiritib, ro'yxatdan o'ting."
        )
    # Foydalanuvchiga xabar yuborish
    await message.answer(response_text)


@dp.message_handler(text="📋 Ro'yxatdan o'tish")
async def ro_tish(message: types.Message):
    await message.answer("Ro'yxatdan o'tish boshlandi")
    await message.answer("Ismingizni kiriting")
    await RegisterState.name.set()


@dp.message_handler(state=RegisterState.name)
async def get_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)

    await message.answer("Endi telefon raqamingizni yuboring:", reply_markup=contact_btn)
    await RegisterState.phone.set()


@dp.message_handler(state=RegisterState.phone, content_types=['contact', 'text'])
async def get_phone(message: types.Message, state: FSMContext):
    if message.contact:
        phone = message.contact.phone_number
        # Oddiy xabar orqali yuborilgan raqam
    else:
        phone = message.text
    if not phone.isdigit() or not phone.startswith("998") or len(phone) != 12:
        await message.answer("Telefon raqami '998XXXXXXXXX' shaklida bo'lishi kerak. Qaytadan kiriting:")
        return
    await state.update_data(phone=phone)
    user_id = message.from_user.id
    username = message.from_user.username or "Noma'lum"

    data = await state.get_data()
    name = data.get("name")
    phone = data.get("phone")

    # Ma'lumotlarni saqlash
    # API'ga foydalanuvchi ma'lumotlarini yuborish
    try:
        response = requests.post(
            f"{API}/users/create/",
            json={
                "telegram_id": user_id,
                "full_name": name,
                "username": username,
                "phone": phone
            }
        )
        if response.status_code == 201:
            await message.answer("✅ Ro'yxatdan muvaffaqiyatli o'tdingiz!", reply_markup=start_btnn)
            # Guruhga xabar yuborish
            group_message = (
                f"Yangi foydalanuvchi ro'yxatdan o'tdi:\n\n"
                f"👤 Ism: {name}\n"
                f"🆔 Username: @{username}\n"
                f"📞 Telefon: {phone}"
            )
            await bot.send_message(GROUP_ID, group_message)
        else:
            # Xato qaytarish
            await message.answer(
                "Xatolik yuz berdi. Ma'lumotlaringizni saqlashda muammo bo'ldi."
            )
    except requests.RequestException as e:
        await message.answer(f"Xatolik yuz berdi. Keyinroq urinib ko'ring.")
    await state.finish()
