import telebot
from telebot import types


class Keyboard(object):
    def __init__(self, view='InLine'):
        if view == 'InLine':
            self.kb_table = types.InlineKeyboardMarkup()
        elif view == 'Reply':
            self.kb_table = types.ReplyKeyboardMarkup()
        pass

    def fill_kb_table(self, table, table_type='table'):
        for i, row in enumerate(table):
            button_list = list()
            for j, column in enumerate(row):
                if table_type == 'contact':
                    button_list.append(types.KeyboardButton(f'{column}',
                                                            request_contact=True))
                elif not column == '-':
                    if j == 0:
                        self.kb_table.add(types.InlineKeyboardButton(f'{column}',
                                                                  callback_data=f'{table_type}{i}{j}'))
                    else:
                        button_list.append(types.InlineKeyboardButton(f'{column}',
                                                                  callback_data=f'{table_type}{i}{j}'))
                else:
                    button_list.append(types.InlineKeyboardButton(f'{column}',
                                                                  callback_data=f'none{i}{j}'))
            self.kb_table.row(*button_list)
        #        self.kb_table.add(types.InlineKeyboardButton('Закончить игру', callback_data='exit'))
        pass

    def get_instant(self):
        return self.kb_table

# def main():
#     bot = telebot.TeleBot('1292821995:AAH-tyF6p0opLx9vtX4W69iC2z30sln9O3U');
#
#     keyboard = Keyboard()
#     keyboard.fill_kb_table([['Тема 1', 100, 200, 300, 400],
#                             ['Тема 2', 100, 200, 300, 400],
#                             ['Тема 3', 100, 200, 300, 400],
#                             ['Тема 4', 100, 200, 300, 400],
#                             ['Тема 5', 100, 200, 300, 400]])
#
#     @bot.callback_query_handler(func=lambda callback_data: True)
#     def callback_worker(callback_data):
#         print(callback_data.data)
#         code = callback_data.data[-2]
#         if code.isdigit():
#             code = int(code)
#             row = code // 10
#             col = code % 10
#         bot.answer_callback_query(callback_data.id)
#
#     @bot.message_handler(commands=['start', 'rm'])
#     def process_start_command(message):
#         print(message.text)
#         if message.text == '/start':
#             bot.send_message(message.from_user.id, "start", reply_markup=keyboard.get_instant())
#         if message.text == '/rm':
#             bot.send_message(message.from_user.id, "rm", reply_markup=types.ReplyKeyboardRemove())
#
#     bot.polling(none_stop=True, interval=0)


# if __name__ == "__main__":
#     main()
