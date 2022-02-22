import requests
from bs4 import BeautifulSoup
from lxml import html
import json
import re

__version__ = 0.0001

header_text = '''   
Host: api.autoteka.ru
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0
Accept: */*
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
Referer: https://autoteka.ru/report/web/uuid/1b3be21f-d62a-4d4e-b9bf-10ec8d8ee7f7
Content-Type: application/x-www-form-urlencoded
X-Client-Version: 9
X-Release-Version: v198
Origin: https://autoteka.ru
Content-Length: 41
Connection: keep-alive
Cookie: u=43d93b27-08a3-468a-85dd-107be3c1c808; tmr_reqNum=59; f=5.cc913c231fb04ced2d6059f4e9572c01357212485bdbc727357212485bdbc727357212485bdbc727357212485bdbc727357212485bdbc727357212485bdbc727357212485bdbc727357212485bdbc727357212485bdbc72734bd85fe5e85ba0346b8ae4e81acb9fa1a2a574992f83a9246b8ae4e81acb9fad99271d186dc1cd0e992ad2cc54b8aa8de9491257467051cc93bf74210ee38d940e3fb81381f3591956cdff3d4067aa559b49948619279117b0d53c7afc06d0b2ebf3cb6fd35a0ac71e7cb57bbcb8e0ff0c77052689da50ddc5322845a0cba1aba0ac8037e2b74f92da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eabdc5322845a0cba1a0df103df0c26013a03c77801b122405c868aff1d7654931c9d8e6ff57b051a5885a344c9a920d8b6f6ea70fc198851d2938bf52c98d70e5cc074a3cd9c0c8bcd4659aa946bf8012b9154f4aaf0a7b4f46ec97e1161e03d77a91940a5dfdfab0646b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acdffbbf3cc0bbfd9c8ef450b311b575812da10fb74cac1eab2da10fb74cac1eab652a613c9379f6818012e98924060d02; _gcl_au=1.1.1996767228.1645535630; ft="+vSvZtvMsdRCcKqn/DU/97FMI56QCt530C2ZKIV7mG7WGKBDDBKi3SgjFlE2wdDc94HI2qDr3NPPNZ3o+tS3xVVJmgDK5BcWU70P3n4GLjAxZFrctI9mPbVdjSVdqQdrett5xsxcdN9X/R9H7LTLd79U342rCUf7qLebNlte2lC8gPuQMbAjP6dysjaTz0hT"; tmr_lvid=e1dc5b816a44e26eeb3d36986cc243d8; tmr_lvidTS=1645535641794; _ga=GA1.2.727362696.1645535644; _gid=GA1.2.1236760406.1645535644; _fbp=fb.1.1645535660343.409025091; adrdel=1; adrcid=Atxz3-UPsScRZ-Wjyurl6pQ; cto_bundle=zo_ddl96eDl3c0pYOUpGV0x4NGpHTkU1ZU5pR3B3NXFmdEMyRHFXbSUyQlljdDlzU3U1VllKYUFrb0FEblV0aG5mUnhKSE1oQml4Z29uN09WU01hM2w2WGlYSzFpMXBCTnM5R3lpU3lIWEVVWFpvRTZIZEFOcHBQSnRscExBWXVDR3YyQUU0QWhpcDBTS09FR2dCUHhVU0NMVGxTSk9PenFRd2ViN0szVWtMbFlBQW05ekdGYVV1Vko4c1FHU0hDQ3RCaFB6aw; auth_access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJTZXNzaW9uSWQiOjU3NTEyNTg2LCJVc2VySWQiOm51bGwsIkF1dGhlbnRpY2F0ZWQiOmZhbHNlLCJEZXZpY2VJZCI6bnVsbCwiZXhwIjoxNjQ1NTQyODg2LCJpYXQiOjE2NDU1NDEwODYsImlzcyI6ImF1dG90ZWthLXBhc3Nwb3J0In0.dTWRpanJvtYRanm5rMRu3WoaalL0QoA-XZyrPo18dPLYW8bMjaSHD5f5NjbMIAAyqlcGOG21ZYI8hi9M7Km04ySUvdFDDyjHhRvUQdJdCCdVyMrD-fFRa0YDH2GD3piMJz2fwdrcjHImleJvFXCEoVZaW7QvFshfGyUfI0EoTQJNARp3sLwTKfxNu9RTAtJx-zKSPTbqauoaXrlIgbvx1UMZyIf5cFcjETnb6W04k6wvAjV-PYvWaW-Dd-SDUXnlMT95fvSXkJeC85tTcfGU6vp-bUdk6J9F3qik3Ht_XpZNoK8HGLq-5YBF0EElKIJklcM8YKOeDpj1zHRHNZazxw; _gat_UA-2546784-18=1; _dc_gtm_UA-78711947-1=1
TE: Trailers
'''.strip()
headers = {}
for string in header_text.split("\n"):
    key, value = string.split(": ")
    headers[key] = value

params = {"uuid": "1b3be21f-d62a-4d4e-b9bf-10ec8d8ee7f7"}


class Parsing:
    def __init__(self, link):
        self.link = link
        self.check_link()

    def check_link(self):
        temp = self.link.lower()
        pattern = "autoteka.ru/report/web/uuid/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
        match = re.search(pattern, temp)
        if match:
            headers["Referer"] = match.group()
            pattern = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
            match = re.search(pattern, temp)
            self.link = "https://api.autoteka.ru/report/uuid/" + match.group() + ".json?csAppCode=webDesktop"
            params["uuid"] = match.group()

        else:
            self.link = None
        pass

    def get_link(self):
        return self.link

    def parse(self):
        # define URL
        if self.link != None:
            # download data
            response = requests.post(url=self.link, headers=headers, json=params)
            print(response.status_code)
            dictionary = response.json()

            if not "error" in dictionary:
                car = {"vin": dictionary["head"]["vin"],
                       "regNumber": dictionary["head"]["regNumber"],
                       "brand": dictionary["head"]["brand"],
                       "model": dictionary["head"]["model"],
                       "year": dictionary["head"]["year"],
                       "createdAt": dictionary["head"]["createdAt"],
                       "uuid": dictionary["head"]["uuid"],
                       }
                return car
        return None