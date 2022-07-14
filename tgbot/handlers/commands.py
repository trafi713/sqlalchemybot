from aiogram.types import Message, CallbackQuery

from tgbot.infrastructure.database.models import User
from tgbot.keyboards.inline import get_manage_commands_keyboard, show_commands_cd


async def show_commands_settings(message: Message, user: User):
    await message.answer("Manage commands", reply_markup=get_manage_commands_keyboard())


async def show_commands(call: CallbackQuery, user: User, callback_data: dict):
    commands_type = callback_data.get("type")
    restricted_type = commands_type == 'restricted'

    commands = '\n'.join([f'/{command.command_text}'
                          for command in user.command_settings
                          if command.restricted == restricted_type])
    if not commands:
        await call.answer("No commands settings")
        return
    await call.answer()

    await call.message.answer("{} commands: {}".format(commands_type.capitalize(), commands))


def register_commands_handlers(dp):
    dp.register_message_handler(show_commands_settings, commands=["commands"])
    dp.register_callback_query_handler(show_commands, show_commands_cd.filter())
