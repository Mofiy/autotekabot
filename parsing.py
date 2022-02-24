import requests
from bs4 import BeautifulSoup
from lxml import html
import json
import re
import logging

__version__ = 0.0002

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


class Parsing:
    def __init__(self, link):
        self.link = link
        self.uuid = ""
        self.params = {"uuid": ""}
        self.API_REQUEST = "https://api.autoteka.ru/report/uuid/{uuid}.json?csAppCode=webDesktop"
        self.API_REFRESH = "https://api.autoteka.ru/user/refresh-session"
        self.cookie = None

    def get_request_link(self):
        return self.API_REQUEST.format(uuid=self.params["uuid"])

    def get_refresh_link(self):
        return self.API_REFRESH

    def check_link(self):
        temp = self.link.lower()
        logging.info(f'PARSER check the link: {temp}')
        pattern = "autoteka.ru/report/web/uuid/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
        match = re.search(pattern, temp)
        if match:
            pattern = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
            match = re.search(pattern, temp)
            result = True
            self.params["uuid"] = match.group()
            self.uuid = match.group()
        else:
            result = False
        return result

    def get_link(self):
        return self.link

    @property
    def parse(self):
        # define URL
        is_correct = self.check_link()
        logging.info(f'PARSER start parsing {self.link}')
        response = None
        if is_correct:
            # download data
            if self.cookie == None:
                response = requests.post(url=self.get_refresh_link())
                logging.info(f'PARSER no cookies make request cookies:{response.status_code}')
                self.cookie = response.cookies

            response = requests.post(url=self.get_request_link(), cookies=self.cookie)
            logging.info(
                f'PARSER web POST request have response code:{response.status_code} and data:{response.text[:100]}')
            if response.status_code == 401:
                logging.info(f'PARSER old cookies make new request:{response.status_code} ')
                response = requests.post(url=self.get_refresh_link())
                self.cookie = response.cookies
                response = requests.post(url=self.get_request_link(), cookies=self.cookie)
                logging.info(
                    f'PARSER web POST repeat request have response code:{response.status_code} ' \
                    f'and data:{response.text[:100]}')
            if response.status_code == 200:
                dictionary = response.json()
                car = {"vin": dictionary["head"]["vin"],
                       "regNumber": dictionary["head"]["regNumber"],
                       "brand": dictionary["head"]["brand"],
                       "model": dictionary["head"]["model"],
                       "year": int(dictionary["head"]["year"]),
                       "createdAt": int(dictionary["head"]["createdAt"]),
                       "uuid": dictionary["head"]["uuid"],
                       }
                logging.info(f'DB parsed {car}')
                return car
            logging.info(
                f'PARSER have problem with web connections')
        return None


if __name__ == "__main__":
    response = requests.post(
        url="https://api.autoteka.ru/report/uuid/5d86cd2f-8ad5-4498-970b-8346c6f6ac3d.json?csAppCode=webDesktop")
    u = response.cookies["u"]
    print(u)
    print(response.status_code)
    print(response.json())
    print(response.history)

    response = requests.post(url="https://api.autoteka.ru/user/refresh-session")
    print(response.cookies)
    print(response.status_code)
    print(response.json())
    print(response.history)

    response = requests.post(
        url="https://api.autoteka.ru/report/uuid/5d86cd2f-8ad5-4498-970b-8346c6f6ac3d.json?csAppCode=webDesktop",
        cookies=response.cookies)
    u = response.cookies["u"]
    print(u)
    print(response.status_code)
    print(response.json())
    print(response.history)
