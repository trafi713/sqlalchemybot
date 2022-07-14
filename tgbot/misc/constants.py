from aiogram.utils.helper import Item, Helper, HelperMode


class Roles(Helper):
    mode = HelperMode.lowerCamelCase

    USER = Item()
    ADMIN = Item()
    BOT_OWNER = Item()

    BLOCKED_USER = Item()
