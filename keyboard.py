from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

__version__ = 0.0002

class Keyboard(object):
    def __init__(self, view='InLine'):
        if view == 'InLine':
            self.kb_table = ReplyKeyboardMarkup()
        pass

    def get_main_menu(self):
        menu = ["Получить данные по VIN или гос.номеру",
                "Загрузить данные c Avtoteka",
                "Узнать баланс RQ",
                "Пригласить друга"]
        for item in menu:
            self.kb_table.add(KeyboardButton(item))
        pass

    def get_ref_menu(self):
        menu = ["Нет пригласителя"]
        for item in menu:
            self.kb_table.add(KeyboardButton(item))
        self.kb_table.one_time_keyboard = True
        pass

    def get_cancel_menu(self):
        menu = ["Вернуться в Основное меню"]
        for item in menu:
            self.kb_table.add(KeyboardButton(item))
        self.kb_table.one_time_keyboard = True
        pass

    def get_instant(self):
        return self.kb_table


if __name__ == "__main__":
    STATES = dict()


    def get_state(id):
        if id in STATES:
            return STATES[id]
        return None


    def set_state(id, state):
        STATES[id] = state

    while True:
        id = input("ID please: ")
        state = input("STATE please: ")

        set_state(id, state)

        print(get_state(id))

        print(STATES)