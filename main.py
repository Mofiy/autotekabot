import os

import telebot.apihelper

from quizclass import Quiz
from keyboard import Keyboard
from wallet import Wallet
import telebot
from telebot import types
import datetime
import logging

__version__ = 0.0001

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class Main(object):
    def __init__(self):
        self.agents = dict()
        # загружаем токен из файла который не сохраняет Git
        token_file = open("token.txt", "r")
        token_string = token_file.readline()
        toket_file.close()
        self.bot = telebot.TeleBot(token_string)
        self.message_to_send = str()
        self.button_row_idx = 0
        self.button_col_idx = 0
        self.wallet = Wallet()
        self.hello_msg = {"hello": "Сообщение когда стартовали бота",}
        pass

    def main(self):

        @self.bot.message_handler(commands=['start', 'help', 'board', 'exit'])
        def process_start_command(message):
            # logging.info(f'MSG : {message.from_user.id} : {message.text}')
            #
            # if message.text == '/start':
            #     if not (message.from_user.id in self.agents):
            #         self.agents.update({message.from_user.id: Quiz()})
            #         keyboard = Keyboard('Reply')
            #         keyboard.fill_kb_table([['Отправить контакт']], 'contact')
            #         self.bot.send_message(message.from_user.id, self.hello_msg, reply_markup=keyboard.get_instant())
            #         self.bot.register_next_step_handler(message, get_number)
            #     else:
            #         self.bot.send_message(message.from_user.id, 'Прежде чем начать заново закончите текущую сессию /exit')
            #         return
            # elif message.text == '/help':
            #     help_msg = "Доступные команды: \n" \
            #                "/help - эта справка\n" \
            #                "/start - начало работы с ботом \n" \
            #                "/board - посмотреть статистику результатов \n" \
            #                "/exit - прервать сессию."
            #     self.bot.send_message(message.from_user.id, help_msg)
            # elif message.text == '/board':
            #     score_msg = self.sc.get_hiscore()
            #     self.bot.send_message(message.from_user.id, score_msg)
            #     pass
            # elif message.text == '/exit':
            #     if message.from_user.id in self.agents.keys():
            #         self.agents[message.from_user.id].end_game_flag = True
            #         self.end_of_the_game(message)
            pass

        def get_number(message):
            # # LOG:
            # logging.info(f'MSG : {message.from_user.id} : {message.text}')
            #
            # if message.text is not None:
            #     keyboard = Keyboard('Reply')
            #     keyboard.fill_kb_table([['Отправить контакт']], 'contact')
            #     self.bot.send_message(message.from_user.id, "Нужно нажать на кнопку и подтвердить передачу контакта.")
            #     self.bot.send_message(message.from_user.id, self.hello_msg, reply_markup=keyboard.get_instant())
            #     self.bot.register_next_step_handler(message, get_number)
            # else:
            #     keyboard = Keyboard()
            #     keyboard.fill_kb_table(self.agents[message.from_user.id].create_rows_cols_pic_box())
            #     self.bot.send_message(message.from_user.id, "Спасибо!", reply_markup=types.ReplyKeyboardRemove())
            #     self.bot.send_message(message.from_user.id, "Выберите вопрос:", reply_markup=keyboard.get_instant())
            #     self.agents[message.from_user.id].user_data.id = message.from_user.id
            #     self.agents[message.from_user.id].user_data.name = message.from_user.username
            #     self.agents[message.from_user.id].status = 1
            #     self.agents[message.from_user.id].user_data.phone = message.json['contact']['phone_number']
            #     self.agents[message.from_user.id].user_data.time = datetime.datetime.now()

        @self.bot.callback_query_handler(func=lambda callback_data: True)
        def callback_worker(callback_data):
            # # LOG:
            # logging.info(f'CALLBACK : {callback_data.from_user.id} : {callback_data.data}')
            # if callback_data.from_user.id not in self.agents:
            #     self.bot.send_message(callback_data.message.chat.id, "Начните с /start  !")
            #     return
            # if callback_data.data.startswith('table'):
            #     if self.agents[callback_data.from_user.id].status != 1:
            #         self.bot.send_message(callback_data.message.chat.id, "Выберите ответ на вопрос!")
            #         return
            #     code = callback_data.data[-2:]
            #     if code.isdigit():
            #         code = int(code)
            #         self.button_row_idx = code // 10
            #         self.button_col_idx = code % 10
            #         if self.button_col_idx == 0:
            #             return
            #         self.agents[callback_data.from_user.id].status = 2
            #         show_question_and_answers(callback_data)
            #     self.bot.answer_callback_query(callback_data.id)
            #     pass
            # elif callback_data.data.startswith('answer'):
            #     if self.agents[callback_data.from_user.id].status != 2:
            #         self.bot.send_message(callback_data.message.chat.id, "Выберите категорию и цену вопроса!")
            #         return
            #     keyboard = Keyboard()
            #     keyboard.fill_kb_table(self.agents[callback_data.from_user.id].create_rows_cols_pic_box())
            #     code = callback_data.data[-2:]
            #     if code.isdigit():
            #         code = int(code)
            #         button_num = code // 10
            #     is_answer_correct, user_answer_msg, correct_answer_msg, full_answer = self.agents[
            #         callback_data.from_user.id].check_answer(button_num)
            #     full_answer = f"Справочная информация:\n{full_answer} \n\n" \
            #                   "/help - для справки по командам"
            #     if is_answer_correct:
            #         msg = f"Это правильный ответ! :\n" \
            #               f"Ваш ответ: {user_answer_msg}\n" \
            #               f"Правильный ответ: {correct_answer_msg}"
            #         self.bot.send_message(callback_data.message.chat.id, msg)
            #         self.bot.send_message(callback_data.message.chat.id, full_answer,
            #                               reply_markup=keyboard.get_instant())
            #     else:
            #         msg = f"Это неправильный ответ! :\n" \
            #               f"Ваш ответ: {user_answer_msg}\n" \
            #               f"Правильный ответ: {correct_answer_msg}"
            #         self.bot.send_message(callback_data.message.chat.id, msg)
            #         self.bot.send_message(callback_data.message.chat.id, full_answer,
            #                               reply_markup=keyboard.get_instant())
            #     self.agents[callback_data.from_user.id].status = 1
            #     if self.agents[callback_data.from_user.id].end_game_flag:
            #         self.end_of_the_game(callback_data)
            pass

        def show_question_and_answers(callback_data):
            # question_msg, answers_list = self.agents[callback_data.from_user.id].get_question_and_answers(
            #     self.button_row_idx, self.button_col_idx - 1)
            # kb = Keyboard()
            # kb.fill_kb_table(answers_list, table_type='answer')
            # self.bot.send_message(callback_data.message.chat.id,
            #                       f"Вопрос №{self.agents[callback_data.message.chat.id].questions_count}\n{question_msg}",
            #                       reply_markup=kb.get_instant())
            pass

        self.bot.polling(none_stop=True, interval=1)
        pass

if __name__ == "__main__":
    bot = Main()
    bot.main()
