from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

start_cd = CallbackData('start', 'action')
show_commands_cd = CallbackData('commands', 'type')


def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Show referral link", callback_data=start_cd.new(action='show_link')),
            ],
            [
                InlineKeyboardButton(text="Show my referrals", callback_data=start_cd.new(action='show_referrals')),
            ],
            [
                InlineKeyboardButton(text="Show my referrer", callback_data=start_cd.new(action='show_referrer')),
            ],
        ]
    )
    return keyboard


def get_manage_commands_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Show allowed commands",
                                     callback_data=show_commands_cd.new(type='allowed')),
            ],
            [
                InlineKeyboardButton(text="Show restricted commands",
                                     callback_data=show_commands_cd.new(type='restricted')),
            ],
        ]
    )
    return keyboard
