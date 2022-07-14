import logging
from typing import Dict, Any

from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import Message

from tgbot.infrastructure.database.functions.settings import check_if_command_restricted


class RestrictionMiddleware(LifetimeControllerMiddleware):
    async def pre_process(self, obj: Message, data: Dict, *args: Any) -> None:
        if isinstance(obj, Message):
            user = data['user']
            session = data['session']
            command = obj.get_command(pure=True)
            restricted_commands = await check_if_command_restricted(session, user.telegram_id, command)
            logging.info(f'Restricted commands: {restricted_commands}')
            if not restricted_commands:
                return

            if restricted_commands:
                await obj.reply('You are not allowed to use this command')
                raise CancelHandler()
