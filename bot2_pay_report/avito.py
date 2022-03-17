import logging
import os
import requests
import json
import time
from dotenv import load_dotenv

__version__ = 0.0001


class Autoteka:
    def __init__(self, client_id, client_secret):
        self.api_url = 'https://pro.autoteka.ru/'
        self.endpoints = {'token': 'token',
                          'active_package': 'autoteka/v1/packages/active_package',
                          'previews': 'autoteka/v1/previews'}
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token, self.expiration, self.token_type = self.get_access_token()

    def get_access_token(self):
        '''
    Получение access token
    Получения временного ключа для авторизации
        :return:
        '''
        url = self.api_url + self.endpoints['token']
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        request_data = {'grant_type': 'client_credentials',
                        "client_id": self.client_id,
                        "client_secret": self.client_secret}

        response = requests.post(url=url, headers=headers, data=request_data)
        if response.status_code == 200:
            answer_json = response.json()
            logging.info(f"AVITO_EXCHANGE: Access_token received: {answer_json}")
            return answer_json['access_token'], \
                   answer_json['expires_in'] + int(time.time()) - 60, \
                   answer_json['token_type']
        logging.error(f"AVITO_EXCHANGE: Can't get access_token! Answer code: {response.status_code}")
        return None

    def get_active_package(self):
        '''
    Метод для запроса остатка отчётов в текущем пакете пользователя

        '''
        header = {"Authorization": self.token_type + ' ' + self.access_token, }
        url = self.api_url + self.endpoints['active_package']
        response = requests.get(url=url, headers=header)
        logging.info(f"AVITO_EXCHANGE: Response status code: {response.status_code}")
        if response.status_code == 200:
            answer_json = response.json()
            logging.info(f"AVITO_EXCHANGE: Active package count received: {answer_json}")
            return answer_json
        elif response.status_code == 403:
            logging.info(f"AVITO_EXCHANGE: Don't have active packages.")
            return 0
        elif response.status_code > 403:
            response_json = response.json()
            logging.error(f"AVITO_EXCHANGE: Request error. Error message: {response_json['error']['message']}")
            return None


    def get_preview_vin(self, vin):
        '''
    Метод для запроса остатка отчётов в текущем пакете пользователя

        '''
        url = self.api_url+self.endpoints['previews']
        headers = {"Content-Type": "application/json",
                   "Authorization": self.token_type + ' ' + self.access_token}
        data = {'vin': vin}
        response = requests.post(url=url, headers=headers, json=json.dumps(data))
        print(response.json())
        # logging.info(f"AVITO_EXCHANGE: Response status code: {response.status_code}")
        # if response.status_code == 200:
        #     answer_json = response.json()
        #     logging.info(f"AVITO_EXCHANGE: Active package count received: {answer_json}")
        #     return answer_json
        # elif response.status_code == 403:
        #     logging.info(f"AVITO_EXCHANGE: Don't have active packages.")
        #     return 0
        # elif response.status_code == 500:
        #     logging.error(f"AVITO_EXCHANGE: Request error.")
        #     return None

    def update_access_token(self):
        #TODO
        pass


logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
# Загрузить данные токена
DOTENV_PATH = "../token.env"
if os.path.exists(DOTENV_PATH):
    load_dotenv(DOTENV_PATH)
else:
    logging.error("Did not find ENV file")
    exit(1)


if __name__ == "__main__":
    autoteka = Autoteka(client_id=os.environ.get('CLIENT_ID'), client_secret=os.environ.get('CLIENT_SECRET'))
    autoteka.get_preview_vin("TSMLYE21S00190068")

