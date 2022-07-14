from sqlalchemy import select, true, insert, update
from sqlalchemy.sql.operators import is_

from tgbot.infrastructure.database.models import User
from tgbot.infrastructure.database.models.settings import CommandSetting, Command, CommandMenu


async def check_if_command_restricted(session, telegram_id, command: str) -> list[str]:
    sql = select(
        CommandSetting.restricted
    ).join(
        User
    ).join(
        Command
    ).where(
        User.telegram_id == telegram_id,
        Command.command_text == command
    )
    return await session.scalar(sql)


async def get_menu_commands(session) -> list[str]:
    sql = select(
        Command.command_text, CommandMenu.description, CommandMenu.lang_code
    ).join(
        CommandMenu
    ).where(
        is_(CommandMenu.in_menu, true())
    ).group_by(
        CommandMenu.lang_code,
        Command.command_text, CommandMenu.description
    )
    return (await session.execute(sql)).all()
#
#
# async def forbid_command(session, telegram_id, command_text):
#     if command_text not in (await get_restricted_commands(session, telegram_id)):
#         sql = insert(CommandSetting).values(
#             telegram_id=telegram_id,
#             command_text=command_text,
#             restricted=True
#         )
#     else:
#         sql = update(CommandSetting).where(
#             CommandSetting.telegram_id == telegram_id,
#             CommandSetting.command_text == command_text
#         ).values(
#             restricted=True
#         )
#
#     await session.execute(sql)
#
#
# async def allow_command(session, telegram_id, command_text):
#     if command_text not in (await get_restricted_commands(session, telegram_id)):
#         sql = insert(CommandSetting).values(
#             telegram_id=telegram_id,
#             command_text=command_text,
#             restricted=True
#         )
#     else:
#         sql = update(CommandSetting).where(
#             CommandSetting.telegram_id == telegram_id,
#             CommandSetting.command_text == command_text
#         ).values(
#             restricted=False
#         )
#
#     await session.execute(sql)
