import telebot
import quizpic
from io import BytesIO

TOKEN = '5055815891:AAFRb4lhTCqRtUdoEF2SPQWhMpRwB2Uk_Ak'
tb = telebot.TeleBot(TOKEN)


@tb.message_handler(commands=['start'])
def start_handler(message):
    msg = tb.send_message(message.chat.id, 'Привет,' + str(message.chat.id))
    tb.register_next_step_handler(msg, auth)


@tb.message_handler(content_types=['text'])
def auth(message):
    tb.send_message(message.chat.id, r'Таблица')
    category = quizpic.get_test_category()
    im1 = quizpic.get_table_board(category)
    bio = BytesIO()
    bio.name = 'image.jpeg'
    im1.save(bio, 'JPEG')
    bio.seek(0)
    tb.send_photo(message.chat.id, photo=bio)


tb.polling(none_stop=True, interval=0)
