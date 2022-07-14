import re

from aiogram.dispatcher.filters import RegexpCommandsFilter, Command
from aiogram.types import Message

from tgbot.infrastructure.database.functions.users import change_balance, get_balance
from tgbot.infrastructure.database.models import User


async def get_balance_for_user(message: Message, session, user: User):
    balance = await get_balance(session, user.telegram_id)
    await message.answer(f'Your balance is: {balance}')


async def increase_balance_handler(message: Message, session, user: User, regexp_command: re.search):
    amount = float(regexp_command.group(1))

    await change_balance(session, user.telegram_id, amount, description='Increased from handler')
    await session.commit()

    balance = await get_balance(session, user.telegram_id)

    await message.answer(f'Increased balance by {amount}. New balance: {balance}')


async def decrease_balance_handler(message: Message, session, user: User, regexp_command: re.search):
    amount = -float(regexp_command.group(1))
    await change_balance(session, user.telegram_id, amount, description='Decreased from handler')
    await session.commit()

    balance = await get_balance(session, user.telegram_id)

    await message.answer(f'Decreased balance by {amount}. New balance: {balance}')


def register_handlers_balance(dp):
    dp.register_message_handler(increase_balance_handler, RegexpCommandsFilter([r'\/increase_balance (\d+\.?\d*)']))
    dp.register_message_handler(decrease_balance_handler, RegexpCommandsFilter([r'\/decrease_balance (\d+\.?\d*)']))
    dp.register_message_handler(get_balance_for_user, Command('get_balance'))
