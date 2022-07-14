import typing

from aiogram.dispatcher.filters import BoundFilter
from aiogram.dispatcher.handler import ctx_data

from tgbot.infrastructure.database.models import User
from tgbot.misc.constants import Roles


class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: typing.Optional[bool] = None):
        self.is_admin = is_admin

    async def check(self, obj):
        if self.is_admin is None:
            return False
        data = ctx_data.get()
        user: User = data.get('user')
        return (user.role == Roles.ADMIN) == self.is_admin
