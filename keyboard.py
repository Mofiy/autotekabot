from aiogram import types
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


class Keyboard(object):
    def __init__(self, view='InLine'):
        if view == 'InLine':
            # self.kb_table = InlineKeyboardMarkup()
        # elif view == 'Reply':
            self.kb_table = ReplyKeyboardMarkup()
        pass

    def get_main_menu(self, message):
        menu = ["Получить данные по VIN",
                "Загрузить данные c Avtoteka",
                "Узнать баланс RQ",
                "Пригласить друга"]
        for item in menu:
            self.kb_table.add(KeyboardButton(item))

        message.reply("Основное меню", reply_markup=self.kb_table)
        pass

