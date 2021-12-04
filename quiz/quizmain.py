from keyboard import Keyboard
from quizclass import Quiz
import telebot
from telebot import types
from user import User

__version__ = 0.0001


class QuizMain(object):
    def __init__(self):
        self.quiz = Quiz()
        self.keyboard = Keyboard()
        self.bot = telebot.TeleBot('1292821995:AAH-tyF6p0opLx9vtX4W69iC2z30sln9O3U');
        self.message_to_send = str()
        self.button_row_idx = 0
        self.button_col_idx = 0

        # self.bot_logic_initialization()
        pass

    def main(self):
        """ 1. init bot logic """
        data_str, _ = self.quiz.create_rows_cols_pic_box()
        self.keyboard.fill_kb_table(data_str)

        @self.bot.message_handler(commands=['start', 'rm'])
        def process_start_command(message):
            print(message.text)
            hello_msg = "Привет, я Одиссей, чат-бот созданный для обучения кибербезопасности. " \
                        "Мой тёзка придумал Троянского коня, а я помогу Вам защитится от троянов!\n" \
                        "Отвечайте на вопросы, а мы поможем вам улучшить ваши знания в этой области\n"

            if message.text == '/start':
                self.bot.send_message(message.from_user.id, hello_msg)
                self.bot.send_message(message.from_user.id, '_', reply_markup=self.keyboard.get_instant())
            if message.text == '/rm':
                self.bot.send_message(message.from_user.id, "rm", reply_markup=types.ReplyKeyboardRemove())
            pass

        @self.bot.callback_query_handler(func=lambda callback_data: True)
        def callback_worker(callback_data):
            print(callback_data.data)
            if callback_data.data.startswith('table'):
                code = callback_data.data[-2:]
                if code.isdigit():
                    code = int(code)
                    self.button_row_idx = code // 10
                    self.button_col_idx = code % 10
                    if self.button_col_idx == 0:
                        return
                    show_question_and_answers(callback_data)
                self.bot.answer_callback_query(callback_data.id)
                pass
            elif callback_data.data.startswith('answer'):
                code = callback_data.data[-2:]
                if code.isdigit():
                    code = int(code)
                    button_num = code // 10
                is_answer_correct, user_answer_msg, correct_answer_msg = self.quiz.check_answer(self.button_row_idx,
                                                                                                self.button_col_idx,
                                                                                                button_num)
                if is_answer_correct:
                    msg = f"Это правильный ответ! :\n" \
                          f"Ваш ответ: {user_answer_msg}\n" \
                          f"Правильный ответ: {correct_answer_msg}"
                    self.bot.send_message(callback_data.message.chat.id, msg)
                    self.bot.send_message(callback_data.message.chat.id,'_', reply_markup=self.keyboard.get_instant())
                else:
                    msg = f"Это неправильный ответ! :\n" \
                          f"Ваш ответ: {user_answer_msg}\n" \
                          f"Правильный ответ: {correct_answer_msg}"
                    self.bot.send_message(callback_data.message.chat.id, msg)
                    self.bot.send_message(callback_data.message.chat.id,'_', reply_markup=self.keyboard.get_instant())
                data_str, _ = self.quiz.create_rows_cols_pic_box()
                self.keyboard.fill_kb_table(data_str)

        # bot.register_next_step_handler(message, get_name)

        def show_question_and_answers(callback_data):
            question_msg, answers_list = self.quiz.get_question_and_answers(self.button_row_idx-1, self.button_col_idx-1)
            print(answers_list)
            kb = Keyboard()
            kb.fill_kb_table(answers_list, table_type='answer')
            self.bot.send_message(callback_data.message.chat.id, f"Вопрос:\n{question_msg}",
                                  reply_markup=kb.get_instant())
            # self.bot.register_next_step_handler(question_msg, get_name)
            pass

        self.bot.polling(none_stop=True, interval=0)
        pass


if __name__ == "__main__":
    quiz = QuizMain()
    quiz.main()
