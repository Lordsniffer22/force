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
from rave_python import Rave, RaveExceptions, Misc
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
import keybds
import bond
import importlib


load_dotenv()
TOKENX = os.getenv('QUIK_TOKEN')
dp = Dispatcher()
bot = Bot(token=TOKENX, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
#Flutter
SECRET = os.getenv('RAVE_SECRET_KEY')
rave = Rave("FLWPUBK-1ab67f97ba59d47b65d67001eb794a05-X", SECRET, production=True)
TESLASSH = int(os.getenv('ADMIN_CHAT_ID'))

UDP_CUSTOM = '-1001653400671'
UDP_REQUEST = '-1002036959256'
force_msg1 = {}
user_states = {}
STATE_NONE = 'none'
MOMO_STATE = 'awaiting_number'
PREMIUM_STATE = 'awaiting_prem'
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

@dp.message(F.text.lower() == '🔐password')
async def send_passwds(message: Message):
    user_id = message.from_user.id
    password = bond.Pass
    if (await check_subscription(UDP_CUSTOM, user_id) and await check_subscription(UDP_REQUEST, user_id)):
        await message.reply(f'<b>Current password:</b> <code>{password}</code>\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n'
                                   '<b><i>Get more channel subs using this bot.</i></b>', reply_markup=keybds.promote.as_markup())
    else:
        force = await message.reply(
            "You must first be a Member in these Channels. Please join the channels to proceed.",
            reply_markup=keybds.builder.as_markup())
@dp.message(F.text.startswith('/pass'))
async def password_set(message: Message):
    msg = message.text
    parts = msg.split()
    user_id = message.from_user.id
    if user_id == TESLASSH:
        with open('bond.py', 'r+') as f:
            content = f.read()
            contents = f"Old {content}"
        await message.reply(contents)
        await asyncio.sleep(2)
        passwd = parts[1]
        with open('bond.py', 'w+') as f:
            f.write(f"Pass = '{passwd}'")
        await message.answer(f"New Password set to: <code>{passwd}</code>")
        importlib.reload(bond)
    else:
        thief = 'Are you a thief?'
        await message.reply(thief)

@dp.message(F.text.lower() == '⚙️fix udp')
async def activator(message: Message):
    Fixing = (f"<b>Hello, {message.from_user.first_name}!</b>\n\n"
              f"Airtel UG got issues with their network since May of 2024. So all they had was to re-route their network traffic through a different channel, leaving its registries not updated.\n"
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
              f"We shall only charge you UGX 5000/= if you choose to re-activate your udp with us, and its only Payable once!. \n"
              f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
              f"⭕️ Are you ready to continue?")
    await message.reply(Fixing, reply_markup=keybds.ready.as_markup())

@dp.message(F.text.lower() == '⚡️premium')
async def premiumfile(message: Message):
    msg = ('A premium file is always valid for 31 days.\n'
           '➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n'
           'What to expect:\n'
           '-Super stable speeds\n'
           '-24/7 admin support\n'
           '-Free UDP activation\n'
           '➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n'
           'Press the button below to Make payment')
    await message.reply(msg, reply_markup=keybds.buy_file.as_markup())
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
    await query.message.delete()
    await query.answer('⭕️ Waiting for Your Payment')
    user_states[user_id] = state
    killed = await bot.send_message(user_id,
                           'Please enter your phone number in the format:\n\n <i>07XXXXXX or 02XXXXXX or 03XXXXXX</i>:',
                           parse_mode=ParseMode.HTML)
    kill_msg[user_id] = killed

@dp.callback_query(lambda query: query.data == 'file')
async def make_charge(query: CallbackQuery):
    global kill_msg
    user_id = query.from_user.id
    state = PREMIUM_STATE
    await query.message.delete()
    await query.answer('⭕️ Waiting for Your Payment')
    user_states[user_id] = state
    killed = await bot.send_message(user_id,
                           'Please enter your phone number in the format:\n\n <i>07XXXXXX or 02XXXXXX or 03XXXXXX</i>:')
    kill_msg[user_id] = killed

txRef = {}

@dp.message(lambda message: user_states.get(message.chat.id) in MOMO_STATE)
async def handle_phone_number(message: types.Message):
    global txRef
    phone_number = message.text
    user_id = message.chat.id
    state = user_states.get(user_id)
    amount = 0

    if state == MOMO_STATE:
        amount = 5000
    try:
        if (phone_number.startswith('07') or phone_number.startswith('02') or phone_number.startswith('03')) and len(phone_number) == 10:
            user_states[user_id] = STATE_NONE
            killed = kill_msg[user_id]
            await asyncio.sleep(4)
            await killed.delete()
            suga = await message.reply('Obtaining your OTP...')
            txRefx = f"{Misc.generateTransactionReference(merchantId=None)}{user_id}"

            payload = {user_id: {

                    "amount": amount,
                    "phonenumber": phone_number,
                    "email": "bots@udpcustom.com",
                    "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
                    "IP": "",
                    "txRef": txRefx
                }
            }
            txRef[user_id] = payload[user_id]['txRef']

            try:
                res = rave.UGMobile.charge(payload[user_id])
                print(res)
                pay_link = res['link']
                builder = InlineKeyboardBuilder()
                markup = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='⭕️ Pay Now', url=pay_link)]
                ])
                builder.attach(InlineKeyboardBuilder.from_markup(markup))

                paid = InlineKeyboardBuilder()
                markup = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Done Paying ✅', callback_data='done'),
                     InlineKeyboardButton(text='⭕️ Pay Now', url=pay_link)]
                ])  # Some markup
                paid.attach(InlineKeyboardBuilder.from_markup(markup))


                rio = await bot.send_message(user_id, f"Use the <u>Flutterwave OTP</u> You just received.\n"
                                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
                                                      f"<i><b>OTP</b> expires in 5 minutes</i>\n"
                                                      f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
                                                      f" Click the <b><i>Pay Now</i></b> Button below.",
                                             parse_mode=ParseMode.HTML, reply_markup=builder.as_markup())
                await asyncio.sleep(3)
                await suga.delete()
                await asyncio.sleep(18)
                #present the Done button instead.
                rio2 = await rio.edit_reply_markup(reply_markup=paid.as_markup())


                #status = res['transaction status']
                #print(status)
                #if status == 'pending':

                #await check_pay_status(user_id, trx)

            except RaveExceptions.TransactionChargeError as e:
                await bot.send_message(user_id, f"Transaction Charge Error: {e.err}")
            except RaveExceptions.TransactionVerificationError as e:
                await bot.send_message(user_id, f"Transaction Verification Error: {e.err['errMsg']}")
        else:
            await bot.send_message(user_id,
                                   'Invalid phone number format. Please enter the phone number in the format 07XXXXXX:')
    except Exception as e:
        await message.answer(f"I got this error:\n\n{e}")



@dp.message(lambda message: user_states.get(message.chat.id) in PREMIUM_STATE)
async def handle_phone_number(message: types.Message):
    global txRef
    phone_number = message.text
    user_id = message.chat.id
    state = user_states.get(user_id)
    amount = 0

    if state == PREMIUM_STATE:
        amount = 7000
    try:
        if (phone_number.startswith('07') or phone_number.startswith('02') or phone_number.startswith('03')) and len(phone_number) == 10:
            user_states[user_id] = STATE_NONE
            killed = kill_msg[user_id]
            await asyncio.sleep(4)
            await killed.delete()
            suga = await message.reply('Obtaining your OTP...')
            txRefx = f"{Misc.generateTransactionReference(merchantId=None)}{user_id}"

            payload = {user_id: {

                    "amount": amount,
                    "phonenumber": phone_number,
                    "email": "premium@udpcustom.com",
                    "redirect_url": "https://rave-webhook.herokuapp.com/receivepayment",
                    "IP": "",
                    "txRef": txRefx
                }
            }
            txRef[user_id] = payload[user_id]['txRef']

            try:
                res = rave.UGMobile.charge(payload[user_id])
                print(res)
                pay_link = res['link']
                builder = InlineKeyboardBuilder()
                markup = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='⭕️ Pay Now', url=pay_link)]
                ])
                builder.attach(InlineKeyboardBuilder.from_markup(markup))

                paid = InlineKeyboardBuilder()
                markup = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text='Done Paying ✅', callback_data='done2'),
                     InlineKeyboardButton(text='⭕️ Pay Now', url=pay_link)]
                ])  # Some markup
                paid.attach(InlineKeyboardBuilder.from_markup(markup))


                rio = await bot.send_message(user_id, f"Use the <u>Flutterwave OTP</u> You just received.\n\n"
                                                      f"<i><b>OTP</b> expires in 5 minutes</i>\n"
                                                      f" Click the <b><i>Pay Now</i></b> Button below.",
                                             parse_mode=ParseMode.HTML, reply_markup=builder.as_markup())
                await asyncio.sleep(3)
                await suga.delete()
                await asyncio.sleep(18)
                #present the Done button instead.
                rio2 = await rio.edit_reply_markup(reply_markup=paid.as_markup())


                #status = res['transaction status']
                #print(status)
                #if status == 'pending':

                #await check_pay_status(user_id, trx)

            except RaveExceptions.TransactionChargeError as e:
                await bot.send_message(user_id, f"Transaction Charge Error: {e.err}")
            except RaveExceptions.TransactionVerificationError as e:
                await bot.send_message(user_id, f"Transaction Verification Error: {e.err['errMsg']}")
        else:
            await bot.send_message(user_id,
                                   'Invalid phone number format. Please enter the phone number in the format 07XXXXXX:')
    except Exception as e:
        await message.answer(f"I got this error:\n\n{e}")


@dp.callback_query(lambda query: query.data == 'done')
async def done_paying(query: CallbackQuery):
    await query.message.delete()
    check = await query.message.answer("Alright!\n\n"
                               "Let me confirm that first...")
    try:
        user_id = query.from_user.id
        txref = txRef.get(user_id, f"Nothing seen for this user_id {user_id}")
        res = rave.UGMobile.verify(txref)
        #print(res)
        if res.get('transactionComplete', False):
            await asyncio.sleep(3)
            await check.delete()
            await query.message.answer('Your payment has been approved!\n\nSend KYC as the message to 175. \nMake sure you send with airtel')
    except Exception as e:
        await asyncio.sleep(3)
        await check.delete()
        dfr = await query.message.answer(f"Oh ooh..\n\nYou have not paid yet. The clock is ticking. \n\nI will tell my creator about this")
        await asyncio.sleep(10)
        await dfr.delete()

@dp.callback_query(lambda query: query.data == 'done2')
async def done_paying(query: CallbackQuery):
    await query.message.delete()
    check = await query.message.answer("Alright!\n\n"
                               "Let me confirm that first...")
    try:
        user_id = query.from_user.id
        txref = txRef.get(user_id, f"Nothing seen for this user_id {user_id}")
        res = rave.UGMobile.verify(txref)
        #print(res)
        if res.get('transactionComplete', False):
            await asyncio.sleep(3)
            await check.delete()
            await query.message.answer('Your payment has been approved!\n'
                                       '➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n'
                                       'Inbox the Admin right now\n'
                                       '--> @teslassh or @hackwell101 for the file')

            await bot.send_message(TESLASSH, f"<b>A user named:</b> {query.from_user.first_name}\n"
                                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
                                             f"<b>Username:</b> {query.from_user.username}\n"
                                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
                                             f"<b>Has made a successful payment.</b>\n"
                                             f"<b>Transaction ID:</b> \n"
                                             f"{txref}\n"
                                             f"➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n"
                                             f"HE NEEDS A FILE.")
    except Exception as e:
        await asyncio.sleep(3)
        await check.delete()
        dfr = await query.message.answer(f"Oh ooh..\n\nYou have not paid yet. The clock is ticking. \n\nI will tell my creator about your intentions")
        await asyncio.sleep(10)
        await dfr.delete()


@dp.callback_query(lambda query: query.data == 'promo')
async def channels(query: CallbackQuery):
    await query.message.delete()
    await query.message.answer('Good start!\n\n'
                               'Contact the Bot developer\n'
                               '╰┈➤ @teslassh')
@dp.callback_query(lambda query: query.data == 'verify')
async def verifs(query: CallbackQuery):
    user_id = query.from_user.id
    password = bond.Pass
    await query.message.delete()
    delet = await query.message.answer('Okay, Hold on a second...')
    await asyncio.sleep(4)
    await delet.delete()
    if (await check_subscription(UDP_CUSTOM, user_id) and await check_subscription(UDP_REQUEST, user_id)):
        await query.message.answer(f'<b>Current password:</b> <code>{password}</code>\n➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖➖\n\n'
                                   '<b><i> Get more channel subs using this bot.</i></b>', reply_markup=keybds.promote.as_markup())
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
