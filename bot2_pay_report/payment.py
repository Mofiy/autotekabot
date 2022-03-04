import asyncio
import logging
import os

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType

from dotenv import load_dotenv

__version__ = 0.0001

help_message = '''
Через этого бота можно купить машину времени, чтобы посмотреть, как происходит покупка и оплата в Telegram.
Отправьте команду /buy, чтобы перейти к покупке.
Узнать правила и положения можно воспользовавшись командой /terms.
'''

start_message = 'Привет! Это демонстрация работы платежей в Telegram!\n' + help_message

pre_buy_demo_alert = '''\
Так как сейчас я запущен в тестовом режиме, для оплаты нужно использовать карточку с номером `4242 4242 4242 4242`
Счёт для оплаты:
'''

terms = '''\
*Спасибо, что выбрали нашего бота. Мы надеемся, вам понравится ваша новая машина времени!*
1. Если машина времени не будет доставлена вовремя, пожалуйста, произведите переосмысление вашей концепции времени и попробуйте снова.
2. Если вы обнаружите, что машина времени не работает, будьте добры связаться с нашими сервисными мастерскими будущего с экзопланеты Trappist-1e. Они будут доступны в любом месте в период с мая 2075 года по ноябрь 4000 года нашей эры.
3. Если вы хотите вернуть деньги, будьте так любезны подать заявку вчера, и мы немедленно совершим возврат.
'''

tm_title = 'Отчет по автомобилю с Автотека'
tm_description = '''\
Актуальный отчет с системы Автотека по минимально возможной цене.
'''

AU_error = '''\
К сожалению, наши курьеры боятся кенгуру, а телепорт не может так далеко отправлять.
Попробуйте выбрать другой адрес!
'''

wrong_email = '''\
Нам кажется, что указанный имейл не действителен.
Попробуйте указать другой имейл
'''

successful_payment = '''
Ура! Платеж на сумму `{total_amount} {currency}` совершен успешно! !
Правила возврата средств смотрите в /terms
Купить ещё одну машину времени своему другу - /buy
'''


MESSAGES = {
    'start': start_message,
    'help': help_message,
    'pre_buy_demo_alert': pre_buy_demo_alert,
    'terms': terms,
    'tm_title': tm_title,
    'tm_description': tm_description,
    'AU_error': AU_error,
    'wrong_email': wrong_email,
    'successful_payment': successful_payment,
}

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)

# Загрузить данные токена
DOTENV_PATH = "../token.env"
if os.path.exists(DOTENV_PATH):
    load_dotenv(DOTENV_PATH)
else:
    logging.error("Did not find ENV file")
    exit(1)


loop = asyncio.get_event_loop()
bot = Bot(os.environ.get('BOT_TOKEN'), parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(bot, loop=loop)

# Setup prices
PRICE = types.LabeledPrice(label='Отчет об автомобиле', amount=6000)


@dp.message_handler(commands=['terms'])
async def process_terms_command(message: types.Message):
    await message.reply(MESSAGES['terms'], reply=False)


@dp.message_handler(commands=['buy'])
async def process_buy_command(message: types.Message):
    if os.environ.get('PAYMENTS_PROVIDER_TOKEN').split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'])

    await bot.send_invoice(message.chat.id,
                           title=MESSAGES['tm_title'],
                           description=MESSAGES['tm_description'],
                           provider_token=os.environ.get('PAYMENTS_PROVIDER_TOKEN'),
                           currency='RUB',
                           photo_url=os.environ.get('AUTOTEKA_URL'),
                           photo_height=512,  # !=0/None, иначе изображение не покажется
                           photo_width=512,
                           photo_size=512,
                           is_flexible=False,  # True если конечная цена зависит от способа доставки
                           prices=[PRICE],
                           start_parameter='time-machine-example',
                           payload='some-invoice-payload-for-our-internal-use'
                           )


@dp.pre_checkout_query_handler(run_task=lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    print('successful_payment:')
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    await bot.send_message(
        message.chat.id,
        MESSAGES['successful_payment'].format(
            total_amount=message.successful_payment.total_amount // 100,
            currency=message.successful_payment.currency
        )
    )


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop)