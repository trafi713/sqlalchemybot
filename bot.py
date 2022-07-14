import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.config import load_config, Config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.balances import register_handlers_balance
from tgbot.handlers.commands import register_commands_handlers
from tgbot.handlers.echo import register_echo
from tgbot.handlers.errors import register_errors
from tgbot.handlers.user import register_user
from tgbot.infrastructure.database.functions.settings import get_menu_commands
from tgbot.infrastructure.database.functions.setup import create_session_pool
from tgbot.middlewares.database import DatabaseMiddleware
from tgbot.middlewares.evnironment import EnvironmentMiddleware
from tgbot.middlewares.restriction import RestrictionMiddleware
from tgbot.services.broadcaster import broadcast
from tgbot.services.init_bot_admins import assign_admin_roles
from tgbot.services.set_commands import set_default_commands

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, session_pool, environment: dict):
    dp.setup_middleware(DatabaseMiddleware(session_pool))
    dp.setup_middleware(EnvironmentMiddleware(**environment))
    dp.setup_middleware(RestrictionMiddleware())


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_commands_handlers(dp)
    register_handlers_balance(dp)
    register_errors(dp)

    register_echo(dp)


async def on_startup(session_pool, bot: Bot, config: Config):
    logger.info("Bot started")
    session: AsyncSession = session_pool()

    # Here we create users in DB and assign them admin roles
    await assign_admin_roles(session, bot, config.tg_bot.admin_ids)
    await broadcast(bot, config.tg_bot.admin_ids, "Bot started")
    commands = await get_menu_commands(session)
    await set_default_commands(bot, commands)
    await session.close()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config
    session_pool = await create_session_pool(config.db, echo=True)

    register_all_middlewares(
        dp,
        session_pool=session_pool,
        environment=dict(config=config)
    )
    register_all_filters(dp)
    register_all_handlers(dp)

    await on_startup(session_pool, bot, config)
    # start
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
