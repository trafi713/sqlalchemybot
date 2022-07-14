from collections import defaultdict

from aiogram import Bot
from aiogram.types import BotCommand

from tgbot.infrastructure.database.models.settings import Command


async def set_default_commands(bot: Bot, commands: list[Command]):
    # Separate commands by lang_code
    commands_by_lang = defaultdict(list)
    for command in commands:
        commands_by_lang[command.lang_code].append(
            BotCommand(
                command=command.command_text,
                description=command.description
            )
        )

    for lang_code, commands in commands_by_lang.items():
        await bot.set_my_commands(commands, language_code=lang_code)
