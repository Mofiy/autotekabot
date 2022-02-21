from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware




import logging
import json
from database import BotDatabase
from keyboard import Keyboard
from messages import MESSAGES
from states import States



__version__ = 0.0001

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
# Загрузить данные токена
token_file = open("token.env", "r")
API_TOKEN = token_file.readline()
token_file.close()

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN[14:-1])
dp = Dispatcher(bot)

# {"message_id": 7,
#  "from": {
#       "id": 467907567,
#       "is_bot": false,
#       "first_name": "Stanislav",
#       "last_name": "Medvedev",
#       "username": "StasMedv",
#       "language_code": "ru"},
#  "chat": {
#       "id": 467907567,
#       "first_name": "Stanislav",
#       "last_name": "Medvedev",
#       "username": "StasMedv",
#       "type": "private"},
#  "date": 1645326369,
#  "text": "/start",
#  "entities": [{"type": "bot_command", "offset": 0, "length": 6}]}


@dp.message_handler(commands=['start', "no", "exit"])
async def commands_handler(message: types.Message):
    id = message["from"]["id"]
    logging.info(f'message from {id}:{message["from"]["username"]} STATE: {states.get_state(id)}')
    state = states.check_user(id)
    if state == 0:
        if message["text"] == "/start":
            user = {"user_id": id,
                    "user_name": message["from"]["username"],
                    "wallet": 3,
                    "code": id,
                    "inviter": -1}
            result = database.get_user(id)
            await message.reply(MESSAGES["hello1"])
            if result is None:
                states.set_state(id, 1)
                database.save_user(user)
                keyboard = Keyboard()
                keyboard.get_ref_menu()
                await message.answer(MESSAGES["hello2"], reply_markup=keyboard.get_instant())
                return
    elif state == 1:
        if message["text"] == "/exit":
            states.set_state(id, 0)
            keyboard = Keyboard()
            keyboard.get_main_menu()
            await message.answer("Основное меню", reply_markup=keyboard.get_instant())
            return

    states.set_state(id, 0)
    await message.reply(MESSAGES["hello1"])
    keyboard = Keyboard()
    keyboard.get_main_menu()
    await message.reply("Основное меню", reply_markup=keyboard.get_instant())
    return


@dp.message_handler()
async def echo(message: types.Message):
    id = message["from"]["id"]
    logging.info(f'message from {id}:{message["from"]["username"]} STATE: {states.get_state(id)}')
    state = states.check_user(id)

    if state == 0:
        if message.text == "Пригласить друга":
            await message.answer(MESSAGES['referal1'])
            await message.answer(MESSAGES['referal2'].format(code=message["from"]["id"]))
            return

        if message.text == "Узнать баланс RQ":
            user = database.get_user(message["from"]["id"])
            await message.answer(MESSAGES['wallet'].format(rq=user["wallet"]))
            return
    elif state == 1:
        if message.text == "Добавить номер пригласителя":
            states.set_state(id, 1)
            return

        elif message.text == "Нет пригласителя":
            states.set_state(id, 0)
            keyboard = Keyboard()
            keyboard.get_main_menu()
            await message.answer(MESSAGES["ref_info_1"], reply_markup=keyboard.get_instant())
            return
        else:   # думаем что ввели код пригласителя и пытаемся его проверить
            ref = message.text
            if ref.isdigit():
                ref = int(ref)
                ref_user = database.get_user(ref)
                if ref_user in None:
                    await message.reply(MESSAGES["ref_err_1"])
                    return
                else:
                    user = database.get_user(id)
                    if user["inviter"] > 0:
                        await message.reply(MESSAGES["ref_err_2"])
                    else:
                        save_user = {"user_id": user["user_id"],
                                        "user_name": user["user_name"],
                                        "wallet": user["wallet"],
                                        "code": user["code"],
                                        "inviter": ref}
                        database.update_user(save_user)
                        await message.reply(MESSAGES["ref_add"])
                        save_user = {"user_id": ref_user["user_id"],
                                     "user_name": ref_user["user_name"],
                                     "wallet": ref_user["wallet"]+1,
                                     "code": ref_user["code"],
                                     "inviter": ref_user["inviter"]}
                        database.update_user(save_user)
                    states.set_state(id, 0)
                    keyboard = Keyboard()
                    keyboard.get_main_menu()
                    await message.reply("Основное меню", reply_markup=keyboard.get_instant())
                    return
    await message.answer(MESSAGES["error"].format(error=message.text))


if __name__ == "__main__":

    # Менеджер состояний и менеджер базы данных
    states = States()
    database = BotDatabase("database.db")
    executor.start_polling(dp, skip_updates=True)

