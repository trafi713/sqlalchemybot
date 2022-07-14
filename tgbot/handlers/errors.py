import logging

from aiogram import Dispatcher
import aiogram.utils.exceptions

from tgbot.infrastructure.database.functions.users import update_user
from tgbot.infrastructure.database.models import User
from tgbot.misc.constants import Roles


async def errors_handler(update, exception, session):
    if isinstance(exception, aiogram.utils.exceptions.BotBlocked):
        user_id = update.message.from_user.id
        logging.info(f"User {user_id} has blocker the bot")
        await update_user(session, User.telegram_id == user_id, role=Roles.BLOCKED_USER)
        await session.commit()

    logging.exception(f'Update: {update} \n{exception}')


def register_errors(dp: Dispatcher):
    dp.register_errors_handler(errors_handler)
