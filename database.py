import sqlite3
from decimal import Decimal
import logging

__version__ = 0.0003

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


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



        c.execute('''CREATE TABLE IF NOT EXISTS cars (
			vin TEXT PRIMARY KEY, 
			regNumber TEXT, 
			brand TEXT, 
			model TEXT, 
			year INTEGER, 
            createdAt INTEGER,
            uuid TEXT,
            user_id INTEGER
			)''')
        conn.commit()

        logging.info("DB: DB ready to work")

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
        logging.info(f"DB: save user {user}")

    def get_user(self, user_id: int):
        ''' Gets User details from Database '''

        conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        details = c.fetchone()
        result = None
        if details != None:
            result = {"user_id": details["user_id"],
                      "user_name": details["user_name"],
                      "wallet": details["wallet"] + 2,
                      "code": details["code"],
                      "inviter": details["inviter"]}
        logging.info(f"DB: get user {result}")
        return result

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
        logging.info(f"DB: update user {user}")
        conn.commit()

    def save_car(self, car):
        '''Saves a car to the Database'''

        conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        values = (car["vin"],
                  car["regNumber"],
                  car["brand"],
                  car["model"],
                  car["year"],
                  car["createdAt"],
                  car["uuid"],
                  car["user_id"])
        c.execute('INSERT INTO cars VALUES (?, ?, ?, ?, ?, ?, ?, ?)', values)
        conn.commit()
        logging.info(f"DB: save car {car}")

    def get_car(self, data):
        ''' Gets car details from Database '''
        conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute('SELECT * FROM cars WHERE vin = ? OR regNumber = ?', (data, data))
        answer = c.fetchone()
        result = None
        if answer != None:
            result = {
                "vin": answer["vin"],
                "regNumber": answer["regNumber"],
                "brand": answer["brand"],
                "model": answer["model"],
                "year": answer["year"],
                "createdAt": answer["createdAt"],
                "uuid": answer["uuid"],
                "user_id": answer["user_id"]
            }
            logging.info(f"DB: get car with data: ", result)
        else:
            logging.info(f"DB: get car with data: None")
        return result

    def update_car(self, car):
        ''' Updates a car within the Database
            vin TEXT PRIMARY KEY,
			regNumber TEXT,
			brand TEXT,
			model TEXT,
			year INTEGER,
            createdAt INTEGER,
            uuid TEXT,
            user_id INTEGER
            '''
        values = (
            car["regNumber"],
            car["brand"],
            car["model"],
            car["year"],
            car["createdAt"],
            car["uuid"],
            car["user_id"],
            car["vin"])

        conn = sqlite3.connect(self.name, detect_types=sqlite3.PARSE_DECLTYPES)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("UPDATE cars " \
                  "SET regNumber = ?, brand = ?, model = ?, year = ?, createdAt = ?, uuid = ?, user_id = ? " \
                  "WHERE vin = ?", values)
        conn.commit()
        logging.info(f"DB: update car {car}")
