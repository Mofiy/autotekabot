from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.utils.markdown import text, bold, italic, code, pre


class TestStates(Helper):
    mode = HelperMode.snake_case

    STATE_START = ListItem()
    STATE_MAIN_MENU = ListItem()
    STATE = ListItem()
    TEST_STATE_3 = ListItem()
    TEST_STATE_4 = ListItem()
    TEST_STATE_5 = ListItem()

import logging
import json
from database import BotDatabase
from keyboard import Keyboard

__version__ = 0.0001

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

MESSAGES = {"hello": "Привет. Бот рассказывает про себя и спрашивает есть ли у вас реферальная ссылка?\n" \
                     "Если есть пригласитель введите его код в сообщении.\n\n Если нет нажмите /no",
            "referal1": "Для того чтобы пригласить друга перешлите ему сообщение ниже.",
            "referal2": "Вас приглашают в Бот с бесплатной базой Автотеки. Перейдите по ссылке t.me/automechanicbot" \
                        " и при первом старте укажите код друга {code}",
            "wallet": "Ваш баланс {rq} RQ"}

token_file = open("token.env", "r")
API_TOKEN = token_file.readline()
token_file.close()

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN[14:-1])
dp = Dispatcher(bot)

# {"message_id": 7, "from": {"id": 467907567, "is_bot": false, "first_name": "Stanislav", "last_name": "Medvedev",
#                                "username": "StasMedv", "language_code": "ru"},
#      "chat": {"id": 467907567, "first_name": "Stanislav", "last_name": "Medvedev", "username": "StasMedv",
#               "type": "private"}, "date": 1645326369, "text": "/start",
#      "entities": [{"type": "bot_command", "offset": 0, "length": 6}]}



@dp.message_handler(commands=['start', "no"])
async def commands_handler(message: types.Message):
    logging.info(f'message from {message["from"]["id"]}:{message["from"]["username"]}')
    if message["text"] == "/start":
        user = {"user_id": message["from"]["id"],
                "user_name": message["from"]["username"],
                "wallet": 3,
                "code": message["from"]["id"]}
        result = database.GetUser(user["user_id"])
        if result == None:
            database.SaveUser(user)
        await message.reply(MESSAGES["hello"])
    elif message["text"] == "/no":
    return

@dp.message_handler()
async def echo(message: types.Message):
    if message.text == "Пригласить друга":
        await message.answer(MESSAGES['referal1'])
        await message.answer(MESSAGES['referal2'].format(code=message["from"]["id"]))
        keyboard = Keyboard()
        await keyboard.get_main_menu(message)
        return

    if message.text == "Узнать баланс RQ":
        user = database.GetUser(message["from"]["id"])
        await message.answer(MESSAGES['wallet'].format(rq=user["wallet"]))
        keyboard = Keyboard()
        await keyboard.get_main_menu(message)
        return
    await message.answer(message.text)

if __name__ == "__main__":
    database = BotDatabase("database.db")
    executor.start_polling(dp, skip_updates=True)
