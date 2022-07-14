import logging
from typing import Dict, Any

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from aiogram.types import CallbackQuery, Message, Update
from aiogram.types.base import TelegramObject
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.infrastructure.database.functions.users import get_one_user, add_user
from tgbot.infrastructure.database.models import User
from tgbot.misc.constants import Roles


class DatabaseMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["update"]

    def __init__(self, session_pool):
        super().__init__()
        self.__session_pool = session_pool

    async def pre_process(self, obj: [CallbackQuery, Message], data: Dict, *args: Any) -> None:
        session: AsyncSession = self.__session_pool()
        data["session"] = session
        data["session_pool"] = self.__session_pool
        if not getattr(obj, "from_user", None):
            return
        if obj.from_user:
            user = await get_one_user(session, telegram_id=obj.from_user.id)

            if not user:
                user = await add_user(
                    session,
                    telegram_id=obj.from_user.id,
                    first_name=obj.from_user.first_name,
                    last_name=obj.from_user.last_name,
                    username=obj.from_user.username,
                    role=Roles.USER,
                )
                await session.commit()

            data['user'] = user

    async def post_process(self, obj: TelegramObject, data: Dict, *args: Any) -> None:
        if session := data.get("session", None):
            session: AsyncSession
            await session.close()
