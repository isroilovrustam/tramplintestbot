import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from data.config import CHANNELS
from keyboards.inline.subscription_inline import check_button
from utils.misc import subscription
from loader import bot


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
            user_full_name = update.message.from_user.full_name
            if update.message.text in ['/help', '/start']:
                return
        elif update.callback_query:
            user = update.callback_query.from_user.id
            user_full_name = update.callback_query.from_user.full_name
            if update.callback_query.data == "check_subs":
                return
        else:
            return
        result = f"Assalomu alaykum {user_full_name}\n\n"
        result += f"🚫Botdan to'liq foydalanish uchun kanalga obuna bo'ling\n\n"
        result += f"♻️Kanalga obuna bo\'lib \"🔄 Obunani tekshirish\" ni bosing"
        final_status = True
        for channel in CHANNELS:
            status = await subscription.check(user_id=user,
                                              channel=channel)
            final_status *= status
            channel = await bot.get_chat(channel)

        if not final_status:
            await update.message.answer(result, disable_web_page_preview=True, reply_markup=check_button)
            # await update.message.answer('♻️Kanallarga obuna bo\'lib "🔄 Obunani tekshirish" ni bosing')
            raise CancelHandler()
