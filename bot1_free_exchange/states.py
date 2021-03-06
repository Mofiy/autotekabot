# states:
#     0 - just /start or main menu
#     1 - waiting when will send referal numbers
#     2 - waiting when will send request
#     3 - waiting when will send link

import logging

__version__ = 0.0002

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

class States:
    def __init__(self):
        self.STATES = dict()

    def get_state(self, id):
        if id in self.STATES:
            return self.STATES[id]
        else:
            return -1

    def set_state(self, id, state):
        logging.info(f"STATES: set for {id} state: {state} ")
        self.STATES[id] = state

    def check_user(self, id):
        state = self.get_state(id)
        if state == -1:
            self.set_state(id, 0)
            return 0
        else:
            return self.get_state(id)
