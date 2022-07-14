import re

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import get_start_link
from aiogram.utils.markdown import hlink

from tgbot.infrastructure.database.functions.users import update_user, get_one_user, get_count_users
from tgbot.infrastructure.database.models import User
from tgbot.keyboards.inline import get_start_keyboard, start_cd


def get_mention(user: User):
    first_name = user.first_name
    last_name = user.last_name or ''
    return hlink(f'{first_name} {last_name}', f'tg://user?id={user.telegram_id}')


async def user_start(message: Message, session):
    total_users = await get_count_users(session)
    await message.reply("Hello, user! "
                        "\n"
                        f"There are {total_users} users in database now!",
                        reply_markup=get_start_keyboard())


async def show_referral_link(call: CallbackQuery):
    await call.answer()
    referral_link = await get_start_link(f'referral-{call.from_user.id}', encode=True)
    await call.message.answer(f"Your referral link: {referral_link}")


async def show_referrals(call: CallbackQuery, user: User, session):
    await call.answer()
    if user.referrals:
        referrals = '\n'.join(f"{num}. {get_mention(referral)} - {referral.created_at.strftime('%d.%m.%Y %H:%M')}"
                              for num, referral in enumerate(user.referrals, start=1))

        await call.message.answer(f"Your referrals: \n{referrals}")
    else:
        await call.message.answer("You don't have referrals yet!")


async def show_referrer(call: CallbackQuery, user: User):
    await call.answer()

    if user.referrer:
        await call.message.answer(f"Your referrer: {get_mention(user.referrer)}")
    else:
        await call.message.answer("You don't have a referrer!")


async def start_from_referral_link(message: Message, session, user: User, deep_link: re.match):
    if not user.referrer:
        referrer_id = int(deep_link.group(1))
        if referrer_id == user.telegram_id:
            await message.answer("You can't refer yourself!")
            return
        await update_user(session, User.telegram_id == user.telegram_id, referrer_id=referrer_id)
        await session.commit()

        referrer = await get_one_user(session, telegram_id=referrer_id)

        await message.answer(f"Welcome! You have been referred by {get_mention(referrer)}!")
        await message.bot.send_message(referrer.telegram_id, f"You have a new referral: {get_mention(user)}!")
    else:
        await message.answer(f"You have already been referred by {get_mention(user.referrer)}!")


def register_user(dp: Dispatcher):
    dp.register_callback_query_handler(show_referral_link, start_cd.filter(action="show_link"))
    dp.register_callback_query_handler(show_referrals, start_cd.filter(action="show_referrals"))
    dp.register_callback_query_handler(show_referrer, start_cd.filter(action="show_referrer"))
    dp.register_message_handler(start_from_referral_link,
                                CommandStart(deep_link=re.compile(r'referral-(\d+)'), encoded=True))
    dp.register_message_handler(user_start, commands=["user", "start"], state="*")
