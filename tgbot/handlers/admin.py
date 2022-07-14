from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from tgbot.filters.admin import AdminFilter


async def admin_start(message: Message):
    await message.reply("Hello, admin!")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(admin_start, Command(commands=['admin']), AdminFilter(is_admin=True), state="*")
