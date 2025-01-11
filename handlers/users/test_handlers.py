import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import dp, db, bot
from data.config import GROUP_ID, API
from states.profile_state import TestState

# @dp.message_handler(text="📝 Test ishlash")
# async def test(message: types):
#     try:
#         response = requests.get(url=f"{API}/tests/")
#         data = response.json()
#         print(data)
#         if not data:
#             await message.answer("No users found.")
#             return
#         for idx, i in enumerate(data, 1):
#             text = f"Question: {i.get('question', 'Unknown')}\n"
#             text += f"A: {i.get('a', 'Unknown')}\n"
#             text += f"B: {i.get('b', 'Unknown')}\n"
#             text += f"C: {i.get('c', 'Unknown')}\n"
#             text += f"D: {i.get('d', 'Unknown')}\n\n"
#
#             await message.answer(text)
#
#     except Exception as e:
#         await message.answer(f"An error occurred: {e}")


# Ballarni saqlash
user_scores = {}


@dp.message_handler(text="📝 Test ishlash")
async def test(message: types.Message, state: FSMContext):
    try:
        response = requests.get(url=f"{API}/tests/")
        data = response.json()
        user = requests.get(url=f"{API}/users/detail/{message.from_user.id}")
        if user.status_code == 404:
            await message.answer("Siz ro'yxatdan o'tmagansiz!!!")
            return
        user = user.json()
        if user['passed']:
            await message.answer("Siz testdan o'tgansiz")
            return
        if user['score']:
            await message.answer("Qqayta test ishlab bo'lmaydi!")
            return
        if not data:
            await message.answer("Testlar topilmadi.")
            return

        # Foydalanuvchining holatini yangilash
        await state.update_data(tests=data, user_id=message.from_user.id, current_question=0, score=0)
        # Birinchi testni yuborish
        await send_question(message, state)

    except Exception as e:
        await message.answer(f"Xato yuz berdi: {e}")


# Testni yuborish funksiyasi
async def send_question(message: types.Message, state: FSMContext):
    data = await state.get_data()
    tests = data['tests']
    current_question = data['current_question']
    await message.delete()

    if current_question >= len(tests):
        await message.answer(f"Testlar tugadi. Sizning ballaringiz: {data['score']}")
        await state.finish()
        if data['score'] < 50:
            requests.patch(url=f"{API}/users/update/{data['user_id']}/", json={"score": data['score']})
        else:
            requests.patch(url=f"{API}/users/update/{data['user_id']}/", json={"score": data['score'], "passed": True})
        return

    question_data = tests[current_question]

    # Variantlarni Inline tugmalarida ko'rsatish
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(f"A: {question_data.get('a', 'Unknown')}", callback_data=f"answer_a_{current_question}"),
        InlineKeyboardButton(f"B: {question_data.get('b', 'Unknown')}", callback_data=f"answer_b_{current_question}"),
        InlineKeyboardButton(f"C: {question_data.get('c', 'Unknown')}", callback_data=f"answer_c_{current_question}"),
        InlineKeyboardButton(f"D: {question_data.get('d', 'Unknown')}", callback_data=f"answer_d_{current_question}")
    )

    # Savolni yuborish
    question_text = f"Question {current_question + 1}: {question_data.get('question', 'Unknown')}"
    await message.answer(question_text, reply_markup=keyboard)

    # Holatni yangilash
    await TestState.answer.set()


# Javobni olish va keyingi savolga o'tish
@dp.callback_query_handler(lambda c: c.data.startswith('answer_'), state=TestState.answer)
async def handle_answer(callback_query: types.CallbackQuery, state: FSMContext):
    answer = callback_query.data.split('_')[1]  # Javobni ajratish: a, b, c, d
    question_index = int(callback_query.data.split('_')[2])  # Savol indexini olish
    data = await state.get_data()
    tests = data['tests']

    # To'g'ri javobni tekshirish
    correct_answer = tests[question_index].get("answer", None)
    question = tests[question_index]
    selected_answer = answer

    # Ballarni hisoblash
    score = data.get("score", 0)
    if selected_answer == correct_answer:
        score += int(question["ball"])  # To'g'ri javob bo'lsa, 1 ball qo'shish

    await state.update_data(current_question=question_index + 1, score=score)
    await send_question(callback_query.message, state)

    # Javobni olgandan so'ng javob berilmaydigan holda kutish uchun holatni yangilash
    await callback_query.answer()
