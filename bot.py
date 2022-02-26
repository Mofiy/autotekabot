from aiogram import Bot, Dispatcher, executor, types

import logging
from database import BotDatabase
from keyboard import Keyboard
from messages import MESSAGES
from states import States
from parsing import Parsing
import datetime
import os
from dotenv import load_dotenv

__version__ = 0.0005

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
# Загрузить данные токена
DOTENV_PATH = "token.env"
if os.path.exists(DOTENV_PATH):
    load_dotenv(DOTENV_PATH)
else:
    logging.error("Did not find ENV file")
    exit(1)


# Initialize bot and dispatcher
bot = Bot(token=os.environ.get('API_TOKEN'))
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
    logging.info(f'BOT: from {id}:{message["from"]["username"]} message: {message.text}')
    state = states.check_user(id)
    result = database.get_user(id)
    if state == 0:
        if message["text"] == "/start":
            await message.answer(MESSAGES["hello_short"])
            if result is None:
                result = {"user_id": id,
                        "user_name": message["from"]["username"],
                        "wallet": 3,
                        "code": id,
                        "inviter": -1}
                await message.answer(MESSAGES["hello1"])
                database.save_user(result)
            keyboard = Keyboard()
            keyboard.get_main_menu(result)
            await message.answer("Основное меню", reply_markup=keyboard.get_instant())
            return
    elif state in [1, 2, 3]:
        if message["text"] == "/exit":
            states.set_state(id, 0)
            keyboard = Keyboard()
            keyboard.get_main_menu(result)
            await message.answer("Основное меню", reply_markup=keyboard.get_instant())
            return
    states.set_state(id, 0)
    await message.reply(MESSAGES["hello1"])
    keyboard = Keyboard()
    keyboard.get_main_menu(result)
    await message.reply("Основное меню", reply_markup=keyboard.get_instant())
    return


@dp.message_handler()
async def echo(message: types.Message):
    id = message["from"]["id"]
    logging.info(f'BOT: from {id}:{message["from"]["username"]} message: {message.text}')
    state = states.check_user(id)
    result = database.get_user(id)
    if state == 0:
        if message.text == "Получить данные по VIN или гос.номеру":
            states.set_state(id, 2)
            keyboard = Keyboard()
            keyboard.get_cancel_menu()
            await message.answer(MESSAGES['get_request'], reply_markup=keyboard.get_instant())
            return
        elif message.text == "Загрузить данные c Avtoteka":
            states.set_state(id, 3)
            keyboard = Keyboard()
            keyboard.get_cancel_menu()
            await message.answer(MESSAGES['load_car'], reply_markup=keyboard.get_instant())
            return
        elif message.text == "Пригласить друга":
            await message.answer(MESSAGES['referal1'])
            await message.answer(MESSAGES['referal2'].format(code=message["from"]["id"]))
            return
        elif message.text == "Узнать баланс RQ":
            user = database.get_user(message["from"]["id"])
            await message.answer(MESSAGES['wallet'].format(rq=user["wallet"]))
            return
        elif message.text == "Ввести код пригласителя":
            states.set_state(id, 1)
            keyboard = Keyboard()
            keyboard.get_cancel_menu()
            await message.answer(MESSAGES['set_ref'], reply_markup=keyboard.get_instant())
            return
    elif state in [1, 2, 3]:  # обработка основного меню
        if message.text == "Вернуться в Основное меню":
            states.set_state(id, 0)
            keyboard = Keyboard()
            keyboard.get_main_menu(result)
            await message.answer("Основное меню", reply_markup=keyboard.get_instant())
            return
        else:
            if state == 1:
                ref = message.text
                if ref.isdigit():
                    ref = int(ref)
                    ref_user = database.get_user(ref)
                    if ref_user == None:
                        await message.reply(MESSAGES["ref_err_1"])
                    else:
                        if result["inviter"] >= 0:
                            await message.reply(MESSAGES["ref_err_2"])
                        else:
                            result["inviter"] = ref_user["user_id"]
                            database.update_user(result)
                            await message.reply(MESSAGES["ref_add"])
                            ref_user["wallet"] = ref_user["wallet"] + 1
                            database.update_user(ref_user)
                            states.set_state(id, 0)
                            keyboard = Keyboard()
                            keyboard.get_main_menu(result)
                            await message.answer("Основное меню", reply_markup=keyboard.get_instant())
                            return
                else:
                    await message.reply(MESSAGES["ref_code_not_numeric"])
                keyboard = Keyboard()
                keyboard.get_cancel_menu()
                await message.answer(MESSAGES['set_ref'], reply_markup=keyboard.get_instant())
                return

            if state == 2:  # обработка основного меню ввод запроса на поиск отчета
                data = message.text.upper()
                car = database.get_car(data)
                if car == None:
                    await message.answer(MESSAGES["get_error1"])
                else:
                    user = database.get_user(id)
                    if user["wallet"] == 0:
                        await message.answer(MESSAGES["get_car_info"].format(brand=car["brand"],
                                        model=car["model"],
                                        year=car["year"],
                                        createdAt=datetime.datetime.fromtimestamp(car["createdAt"])))
                        await message.answer(MESSAGES["get_error2"])
                    else:
                        await message.answer(MESSAGES["get_car_info"].format(brand=car["brand"],
                                        model=car["model"],
                                        year=car["year"],
                                        createdAt=datetime.datetime.fromtimestamp(car["createdAt"])) + \
                                        "\nhttps://autoteka.ru/report/web/uuid/" + car["uuid"])
                        user["wallet"] = user["wallet"] - 1
                        database.update_user(user)
                    states.set_state(id, 0)
                    keyboard = Keyboard()
                    keyboard.get_main_menu(result)
                    await message.answer("Основное меню", reply_markup=keyboard.get_instant())
                    return
                keyboard = Keyboard()
                keyboard.get_cancel_menu()
                await message.answer(MESSAGES['get_request'], reply_markup=keyboard.get_instant())
                return
            elif state == 3:  # обработка основного меню ввод ссылки на отчет
                link = message.text
                parser = Parsing(link)
                if parser.check_link():
                    car = parser.parse
                    if car is not None:
                        car_in_db = database.get_car(car["vin"])
                        is_new = False
                        if car_in_db == None:
                            car["user_id"] = id
                            database.save_car(car)
                            is_new = True
                        else:
                            if car_in_db["createdAt"] < car["createdAt"]:
                                car["user_id"] = id
                                database.update_car(car)
                                is_new = True
                            else:
                                await message.answer(MESSAGES["load_old_car"])
                        if is_new:
                            save_user = database.get_user(id)
                            database.update_user(save_user)
                            states.set_state(id, 0)
                            keyboard = Keyboard()
                            keyboard.get_main_menu()
                            await message.answer(MESSAGES["load_car_success"], reply_markup=keyboard.get_instant())
                            return
                    else:
                        await message.answer(MESSAGES["load_car_bad_link"])
                else:
                    await message.answer(MESSAGES["load_car_bad_link"])
                keyboard = Keyboard()
                keyboard.get_cancel_menu()
                await message.answer(MESSAGES['load_car'], reply_markup=keyboard.get_instant())
                return
    keyboard = Keyboard()
    keyboard.get_main_menu(result)
    await message.answer(MESSAGES["error"], reply_markup=keyboard.get_instant())



if __name__ == "__main__":
    # Менеджер состояний и менеджер базы данных
    states = States()
    database = BotDatabase("database.db")
    executor.start_polling(dp, skip_updates=True)
