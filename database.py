import sqlite3
from decimal import Decimal


def adapt_decimal(d):
    return format(round(d, 14), 'f')


def convert_decimal(s):
    return Decimal(s)


class BotDatabase:
    def __init__(self, name: str):
        sqlite3.register_adapter(Decimal, adapt_decimal)
        sqlite3.register_converter("decimal", convert_decimal)
        self.name = name
        self.Initialise()

    def Initialise(self):
        ''' Initialises the Database '''

        conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        # Create tables
        c.execute('''CREATE TABLE IF NOT EXISTS users (
			user_id INTEGER PRYMARY KEY, 
			user_name TEXT,
			wallet INTEGER NOT NULL DEFAULT 0,  
			code INTEGER NOT NULL DEFAULT 0,
			inviter INTEGER NOT NULL DEFAULT 0
			)''')

        # 			state integer NOT NULL DEFAUL

        c.execute('''CREATE TABLE IF NOT EXISTS cars (
			id INTEGER PRIMARY KEY AUTOINCREMENT, 
			vin_number TEXT, 
			goverment_number TEXT, 
			body_number TEXT, 
			engine_number TEXT, 
			car_number TEXT, 
            last_date DATE,
            link TEXT,
            from_user INTEGER
			)''')
        conn.commit()

    def save_user(self, user):
        '''
        Adds a User to the Database

			id integer primary key AUTOINCREMENT,
			user_id integer,
			user_name text,
			wallet integer,
			code text
        '''
        conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        values = (user["user_id"],
                  user["user_name"],
                  user["wallet"],
                  user["code"],
                  user["inviter"])
        c.execute('INSERT INTO users VALUES (?, ?, ?, ?, ?)', values)
        conn.commit()

    def get_user(self, user_id: int):
        ''' Gets User details from Database '''

        conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        details = c.fetchone()
        return details

    def update_user(self, user):
        ''' Updates a User within the Database '''

        conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        c.execute("UPDATE users SET " \
                  "user_name = ?, " \
                  "wallet = ?, " \
                  "code = ?, " \
                  "inviter = ? " \
                  "WHERE user_id = ?",
                  (user["user_name"], user["wallet"], user["code"], user["inviter"], user["user_id"]))
        conn.commit()
    #
    # def SaveOrder(self, order):
    #     '''
    #     Saves an Order to the Database
    #     '''
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     values = (
    #         order['id'],
    #         order['bot_id'],
    #         order['symbol'],
    #         order['time'],
    #         order['price'],
    #         order['take_profit_price'],
    #         order['original_quantity'],
    #         order['executed_quantity'],
    #         order['status'],
    #         order['side'],
    #         order['is_entry_order'],
    #         order['is_closed'],
    #         order['closing_order_id']
    #     )
    #     c.execute('INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', values)
    #     conn.commit()
    #
    #
    # def UpdateOrder(self, order):
    #     ''' Updates a Bot within the Database '''
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #
    #     values = (
    #         order['take_profit_price'],
    #         order['executed_quantity'],
    #         order['status'],
    #         order['is_closed'],
    #         order['closing_order_id'],
    #         order['id'])
    #
    #     c.execute('Update orders ' + \
    #               'Set ' + \
    #               'take_profit_price = ?, ' + \
    #               'executed_quantity = ?, status = ?, ' + \
    #               'is_closed = ?, closing_order_id = ? ' + \
    #               'Where id = ?', values)
    #     conn.commit()
    #
    # def SavePair(self, pair):
    #     '''
    #     Saves a Pair to the Database
    #         id text primary key,
    #         bot_id text,
    #         symbol text,
    #         is_active bool,
    #         current_order_id text,
    #         profit_loss text,
    #         FOREIGN KEY(current_order_id) REFERENCES orders(id),
    #     FOREIGN KEY(bot_id) REFERENCES bots(id)
    #     '''
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     values = (
    #         pair['id'],
    #         pair['bot_id'],
    #         pair['symbol'],
    #         pair['is_active'],
    #         pair['current_order_id'],
    #         pair['profit_loss'],
    #     )
    #     c.execute('INSERT INTO pairs VALUES (?, ?, ?, ?, ?, ?)', values)
    #     conn.commit()
    #
    # def GetPair(self, id: str):
    #     ''' Gets Bot details from Database '''
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     c.execute('SELECT * FROM pairs WHERE id=?', (id,))
    #     result = dict(c.fetchone())
    #     return result
    #
    # def UpdatePair(self, bot, symbol, pair):
    #     ''' Updates a Bot within the Database '''
    #     values = (
    #         pair['is_active'],
    #         pair['current_order_id'],
    #         pair['profit_loss'],
    #         symbol,
    #         bot['id'])
    #
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     c.execute("UPDATE pairs " + \
    #               "SET is_active = ?, current_order_id = ?, profit_loss = ? " + \
    #               "WHERE symbol = ? and bot_id = ? ", values)
    #     conn.commit()
    #
    # def GetOpenOrdersOfBot(self, bot):
    #     ''' Gets all the bots within a database '''
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     c.execute('SELECT * FROM orders Where bot_id = ? and closing_order_id = 0 and is_closed = False', (bot['id'],))
    #
    #     orders = []
    #     result = [dict(row) for row in c.fetchall()]
    #     return result
    #
    # def GetActivePairsOfBot(self, bot):
    #     ''' Gets all the bots within a database '''
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     c.execute('SELECT * FROM pairs Where bot_id = ? and is_active = True', (bot['id'],))
    #     result = [dict(row) for row in c.fetchall()]
    #     return result
    #
    # def GetAllPairsOfBot(self, bot):
    #     ''' Gets all the bots within a database '''
    #     conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
    #     conn.row_factory = sqlite3.Row
    #     c = conn.cursor()
    #     c.execute('SELECT * FROM pairs Where bot_id = ?', (bot['id'],))
    #     result = [dict(row) for row in c.fetchall()]
    #     return result


if __name__ == "__main__":
    database = BotDatabase("database.db")
    result = database.Get_user(user_id=467907567)
    print(result['user_name'])
