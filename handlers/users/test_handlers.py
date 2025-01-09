from aiogram import types
from aiogram.dispatcher import FSMContext
from utils.misc.tests import testlar
from loader import dp, db, bot
from keyboards.inline.subscription_inline import ha_yoq
from states.profile_state import RegisterState, TestState
from data.config import GROUP_ID
from keyboards.default.start_button import test_btn, start_btn


@dp.message_handler(text='📋 TEST ISHLASH')
async def bot_start(message: types.Message):
    user_id = message.from_user.id

    # Foydalanuvchini tekshirish
    user = db.select_user(user_id)

    if user:
        await message.answer(f"Test ishlashni boshlaymizmi?", reply_markup=ha_yoq)
    else:
        await message.answer("🚫 Siz hali ro‘yxatdan o‘tmagansiz! Testni ishlashdan oldin ro‘yxatdan o‘ting.")
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


@dp.callback_query_handler(text='yoq')
async def hsa(call: types.CallbackQuery):
    await call.message.answer("Test ishlash bekor qilindi!")
    await call.message.delete()


@dp.callback_query_handler(text='ha')
async def hsa(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer("Test ishlashni boshladik!", reply_markup=test_btn)
    question = testlar['bir']["savol"]
    options = "\n".join([f"A: {testlar['bir']['A']['variant1']}", f"B: {testlar['bir']['B']['variant1']}", f"C: {testlar['bir']['C']['variant1']}",
                         f"D: {testlar['bir']['D']['variant1']}"])

    await call.message.answer(f"1. Savol: {question}\n{options}")
    await TestState.question_1.set()


@dp.message_handler(state=TestState.question_1)
async def answer_fullname(message: types.Message, state: FSMContext):
    question_1 = message.text

    await state.update_data(
        {"question_1": testlar['bir'][question_1]}
    )
    question = testlar['ikki']["savol"]
    options = "\n".join([f"A: {testlar['ikki']['A']['variant1']}", f"B: {testlar['ikki']['B']['variant1']}", f"C: {testlar['ikki']['C']['variant1']}",
                         f"D: {testlar['ikki']['D']['variant1']}"])

    await message.answer(f"2. Savol: {question}\n{options}")
    await TestState.question_2.set()


@dp.message_handler(state=TestState.question_2)
async def answer_fullname(message: types.Message, state: FSMContext):
    question_2 = message.text

    await state.update_data(
        {"question_2": testlar['ikki'][question_2]}
    )
    question = testlar['uch']["savol"]
    options = "\n".join([f"A: {testlar['uch']['A']['variant1']}", f"B: {testlar['uch']['B']['variant1']}", f"C: {testlar['uch']['C']['variant1']}",
                         f"D: {testlar['uch']['D']['variant1']}"])

    await message.answer(f"3. Savol: {question}\n{options}")
    await TestState.question_3.set()


@dp.message_handler(state=TestState.question_3)
async def answer_fullname(message: types.Message, state: FSMContext):
    question_3 = message.text

    await state.update_data(
        {"question_3": testlar['uch'][question_3]}
    )
    question = testlar['uch']["savol"]
    options = "\n".join([f"A: {testlar['tort']['A']['variant1']}", f"B: {testlar['tort']['B']['variant1']}", f"C: {testlar['tort']['C']['variant1']}",
                         f"D: {testlar['tort']['D']['variant1']}"])

    await message.answer(f"4. Savol: {question}\n{options}")
    await TestState.question_4.set()


@dp.message_handler(state=TestState.question_4)
async def answer_fullname(message: types.Message, state: FSMContext):
    question_4 = message.text

    await state.update_data(
        {"question_4": testlar['tort'][question_4]}
    )
    question = testlar['besh']["savol"]
    options = "\n".join([f"A: {testlar['besh']['A']['variant1']}", f"B: {testlar['besh']['B']['variant1']}", f"C: {testlar['besh']['C']['variant1']}",
                         f"D: {testlar['besh']['D']['variant1']}"])

    await message.answer(f"5. Savol: {question}\n{options}")
    await TestState.question_5.set()


@dp.message_handler(state=[TestState.question_5])
async def answer_fullname(message: types.Message, state: FSMContext):
    question_5 = message.text

    await state.update_data(
        {"question_5": testlar['besh'][question_5]}
    )

    data = await state.get_data()
    question_1 = data.get("question_1")
    question_2 = data.get("question_2")
    question_3 = data.get("question_3")
    question_4 = data.get("question_4")
    question_5 = data.get("question_5")
    score = int(question_1['ball']) + int(question_2['ball']) + int(question_3['ball']) + int(question_4['ball']) + int(question_5['ball'])
    msg = f"Score : {score}"
    passed = False
    if score > 2:
        passed = True
    db.update_user(score=score, passed=passed, id=message.from_user.id)
    # user = db.select_user(id=message.from_user.id)
    await message.answer(msg, reply_markup=start_btn)
    await state.finish()
