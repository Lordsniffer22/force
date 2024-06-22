from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


udpcustom = 'udpcustom'
udprex = 'udp_request'
keyb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🔐Password'),
            KeyboardButton(text='⚙️Fix UDP'),
            KeyboardButton(text='⚡️Premium')
        ]

    ],
    resize_keyboard=True
)

admin_keyb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='👨‍👦 Create User'),
            KeyboardButton(text='🙅 kick user'),
            KeyboardButton(text='👩‍👩‍👧 My Clients')
        ],
[
            KeyboardButton(text='💰 Check Bal'),
            KeyboardButton(text='🏧 Pin Gen..'),
            KeyboardButton(text='🆘 Help')
        ]

    ],
    resize_keyboard=True
)
builder = InlineKeyboardBuilder()
markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='UDP Custom', url=f"https://t.me/{udpcustom}"),
     InlineKeyboardButton(text='UDP Request', url=f"https://t.me/{udprex}")],
    [InlineKeyboardButton(text='Verify Membership', callback_data=f'verify')
 ]
])  # Some markup
builder.attach(InlineKeyboardBuilder.from_markup(markup))


ready = InlineKeyboardBuilder()
markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Am ready!', callback_data='am_ready'),
     InlineKeyboardButton(text='Not really', callback_data='not_at_all')]
])  # Some markup
ready.attach(InlineKeyboardBuilder.from_markup(markup))


pay_button = InlineKeyboardBuilder()
markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Mobile Money', callback_data='momo')]
])  # Some markup
pay_button.attach(InlineKeyboardBuilder.from_markup(markup))

promote = InlineKeyboardBuilder()
markup = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⭕️ Promote ⚡️', callback_data='promo')]
])  # Some markup
promote.attach(InlineKeyboardBuilder.from_markup(markup))



