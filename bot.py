from aiogram import Bot, Dispatcher, executor, types

import logging
from database import BotDatabase

__version__ = 0.0001

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

token_file = open("token.env", "r")
API_TOKEN = token_file.readline()
token_file.close()

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN[14:-1])
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        '''
        # Old fashioned way:
        await bot.send_photo(
            message.chat.id,
            photo,
            caption='Cats are here 😺',
            reply_to_message_id=message.message_id,
        )
        '''

        await message.reply_photo(photo, caption='Cats are here 😺')


@dp.message_handler()
async def echo(message: types.Message):


    await message.answer(message.text)

if __name__ == "__main__":
    database = BotDatabase("database.db")
    executor.start_polling(dp, skip_updates=True)
