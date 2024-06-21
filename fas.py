import os
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, types, F
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from rave_python import Rave, RaveExceptions
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
import keybds
load_dotenv()
TOKENX = os.getenv('QUIK_TOKEN')
dp = Dispatcher()
bot = Bot(token=TOKENX, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#Flutter
SECRET = os.getenv('RAVE_SECRET_KEY')
rave = Rave("FLWPUBK-1ab67f97ba59d47b65d67001eb794a05-X", SECRET, production=True)


UDP_CUSTOM = '-1001653400671'
UDP_REQUEST = '-1002036959256'
force_msg1 = {}
user_states = {}
STATE_NONE = 'none'
MOMO_STATE = 'awaiting_number'
print(TOKENX)
async def check_subscription(chat_id: int, user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking subscription status: {e}")
        return False
@dp.message(CommandStart())
async def start_msg(message: Message):
    start_msg = 'Hello, welcome to the Danger zone!\n\nOnly Bad ass dudes know this bot. Go back to your village🤡'
    await message.reply(start_msg, reply_markup=keybds.keyb)

@dp.message(F.text.lower() == 'password')
async def send_passwds(message: Message):
    user_id = message.from_user.id

    if (await check_subscription(UDP_CUSTOM, user_id) and await check_subscription(UDP_REQUEST, user_id)):
        await message.reply('The current password is: <code>@udpcustom</code>')
    else:
        force = await message.reply(
            "You must first be a Member in these Channels. Please join the channels to proceed.",
            reply_markup=keybds.builder.as_markup())
@dp.message(F.text.lower() == 'clone bot')
async def cloner(message: Message):
    await message.reply('This feature is currently unavailable. \n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n'
                        'If you are a channel owner and you want to set this feature too, Please contact @teslassh for assistance')

@dp.message(F.text.lower() == 'fix udp')
async def activator(message: Message):
    Fixing = (f"<b>Hello, {message.from_user.first_name}!</b>\n\n"
              f"Airtel UG got issues with their network since May of 2024. So all they had was to re-route their network traffic through a different channel, leaving its registries not updated.\n"
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
              f"We shall only charge you UGX 5000/= if you choose to re-activate your udp with us, and its only Payable once!. \n"
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
              f"⭕️ Are you ready to continue?")
    await message.reply(Fixing, reply_markup=keybds.ready.as_markup())

@dp.callback_query(lambda query: query.data == 'am_ready')
async def ready(query: CallbackQuery):
    await query.message.delete()
    kill = await query.message.answer('Nice move!\n\nOpening Payments page...')
    await asyncio.sleep(4)
    await kill.delete()
    await query.message.answer('Select your Payment Method', reply_markup=keybds.pay_button.as_markup())

@dp.callback_query(lambda query: query.data == 'not_at_all')
async def not_ready(query: CallbackQuery):
    await query.message.delete()
    kill2 = await query.message.answer('Sorry to hear that.\n\n'
                                       'Lets Catch up Next time😍')
    await asyncio.sleep(4)
    await kill2.delete()



kill_msg = {}
@dp.callback_query(lambda query: query.data == 'momo')
async def make_charge(query: CallbackQuery):
    global kill_msg
    user_id = query.from_user.id
    state = MOMO_STATE
    await query.answer('Please Enter Your Phone number (no country code)')
    user_states[user_id] = state
    killed = await bot.send_message(user_id,
                           'Please enter your phone number in the format:\n\n <i>07XXXXXX or 02XXXXXX or 03XXXXXX</i>:',
                           parse_mode=ParseMode.HTML)
    kill_msg[user_id] = killed


@dp.message(lambda message: user_states.get(message.chat.id) in MOMO_STATE)
async def handle_phone_number(message: types.Message):
    phone_number = message.text
    user_id = message.chat.id
    state = user_states.get(user_id)
    amount = 0

    if state == MOMO_STATE:
        amount = 5000
    try:
        if (phone_number.startswith('07') or phone_number.startswith('02') or phone_number.startswith('03')) and len(
                phone_number) == 10:
            user_states[user_id] = STATE_NONE
            killed = kill_msg[user_id]
            await asyncio.sleep(4)
            await killed.delete()
            suga = await message.reply('Obtaining your OTP...')

            payload = {
                "amount": amount,
                "phonenumber": phone_number,
                "email": "bots@udpcustom.com",
                "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
                "IP": ""
            }

            try:
                res = rave.UGMobile.charge(payload)
                pay_link = res['link']
                builder = InlineKeyboardBuilder()
                markup = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Pay Now', url=pay_link)]
                ])
                builder.attach(InlineKeyboardBuilder.from_markup(markup))
                rio = await bot.send_message(user_id, f"Use the <u>Flutterwave OTP</u> You just received.\n\n"
                                                      f"<i><b>OTP</b> expires in 5 minutes</i>\n"
                                                      f" Click the <b><i>Pay Now</i></b> Button below.",
                                             parse_mode=ParseMode.HTML, reply_markup=builder.as_markup())
                await asyncio.sleep(3)
                await suga.delete()
                await asyncio.sleep(300)
                await rio.delete()
            except RaveExceptions.TransactionChargeError as e:
                await bot.send_message(user_id, f"Transaction Charge Error: {e.err}")
            except RaveExceptions.TransactionVerificationError as e:
                await bot.send_message(user_id, f"Transaction Verification Error: {e.err['errMsg']}")
        else:
            await bot.send_message(user_id,
                                   'Invalid phone number format. Please enter the phone number in the format 07XXXXXX:')
    except Exception as e:
        await message.answer(f"I got this error:\n\n{e}")

@dp.callback_query(lambda query: query.data == 'verify')
async def verifs(query: CallbackQuery):
    user_id = query.from_user.id
    await query.message.delete()
    delet = await query.message.answer('Okay, Hold on a second...')
    await asyncio.sleep(4)
    await delet.delete()
    if (await check_subscription(UDP_CUSTOM, user_id) and await check_subscription(UDP_REQUEST, user_id)):
        await query.message.answer('The current password is: ABCD')
    else:
        await query.message.answer(
            "Not a joke! No passwords unless the condition is met. \n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n👉Join the channels below and try again.",
            reply_markup=keybds.builder.as_markup())
@dp.message()
async def any_other_msgs(message: Message):
    user_id = message.from_user.id
    cmd = message.text
    if (cmd.startswith('07') or cmd.startswith('256')):
        await message.answer('Fuck you bro! Use the buttons to do that')
async def main() -> None:
    await dp.start_polling(bot)

if __name__ == '__main__':
    print('Bot is ready')
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
