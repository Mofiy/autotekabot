import requests
from bs4 import BeautifulSoup
from lxml import html
import json
import re

HEADER = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Connection":"keep-alive",
        "Cookie":"_gcl_au=1.1.819190641.1645524595; f=5.cc913c231fb04ced2d6059f4e9572c01357212485bdbc727357212485bdbc727357212485bdbc727357212485bdbc727357212485bdbc727357212485bdbc727357212485bdbc727357212485bdbc727357212485bdbc72734bd85fe5e85ba0346b8ae4e81acb9fa1a2a574992f83a9246b8ae4e81acb9fad99271d186dc1cd0e992ad2cc54b8aa8de9491257467051cc93bf74210ee38d940e3fb81381f3591956cdff3d4067aa559b49948619279117b0d53c7afc06d0b2ebf3cb6fd35a0ac71e7cb57bbcb8e0ff0c77052689da50ddc5322845a0cba1aba0ac8037e2b74f92da10fb74cac1eab2da10fb74cac1eab2da10fb74cac1eabdc5322845a0cba1a0df103df0c26013a03c77801b122405c868aff1d7654931c9d8e6ff57b051a5885a344c9a920d8b6f6ea70fc198851d2938bf52c98d70e5cc074a3cd9c0c8bcd4659aa946bf8012b9154f4aaf0a7b4f46ec97e1161e03d77a91940a5dfdfab0646b8ae4e81acb9fa46b8ae4e81acb9fa02c68186b443a7acdffbbf3cc0bbfd9c2acc5fc4ea1d4cde2da10fb74cac1eab2da10fb74cac1eabe61a31fbb5a8928cc1757d3fc08ce505b841da6c7dc79d0b; _ga=GA1.2.60402306.1645524602; _gid=GA1.2.1098981484.1645524602; ft=\"7NsdL+GxKKkdANKkekOIQGUtksCRKO0eKOMyWXgCGYsQVRXtqXkf1SaCEcvkDlhPk0lk9hUi0CUM83dLneemzAU8SkYsAzXGWdsuBNzomDOrkLbZw0ldw/2HsD+tHrXKwbcdCR40PZ3nzyhpAs9t+WthWejJIpl55yIx+i2WBk8d0aJ8lWDf1gDmIA4z7KpC\"; tmr_reqNum=11; tmr_lvid=70c5aaab34ccbd2081abf47558ac4e4b; tmr_lvidTS=1645524602785; cto_bundle=rWNZ3F9idm0lMkJZUUwydTdpSkhGR1BkZ2ZHRGh1cmhMZElLUEt2WVMlMkZ3eng1RklkQWp3TzFsZTBhbDVjMVhUZmh0NlpDT0VFdFVQR2UwVENraVdrcEY2UkZXeEtldU54SDZWQlA2JTJGdkV2cmxMV3hvUGhrUlRUJTJCR2JMYnNpNXIzaHozdnFDZDRTMVNxWWNMYmxHelhyOUVLQiUyQnpEUFdzeXQlMkZQNXZQTG94JTJGVWgyZWR4M3dLUVVET3pDJTJGMFNuS0VFMlg1aDMy; u=ee1ce3fd-9753-420e-9ed9-fc54582d8569; auth_access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJTZXNzaW9uSWQiOjU3NDI3NTIzLCJVc2VySWQiOm51bGwsIkF1dGhlbnRpY2F0ZWQiOmZhbHNlLCJEZXZpY2VJZCI6bnVsbCwiZXhwIjoxNjQ1NTI2NDAzLCJpYXQiOjE2NDU1MjQ2MDMsImlzcyI6ImF1dG90ZWthLXBhc3Nwb3J0In0.jj5ZH5Qy0wxTPdIOmMMDnNrJ8jV2V8LklFFM1xvMowq6x63tgR_r3DfW2AGSVZA2MyHqLeEmFLj617M30tKhZyRr8tT__1pdyNt_8zXUADmQThD4Mxb70BGkBr4ZTca9LO4YNZr2maPSO6KxCi9KJlFJ3qACYMCCYDilPmq2P-rOXEuNntIDTjq6_5cQkFtt6fAk9Ck22QZo1n91U0cAAo_ihc9qn-9gennIsESsHZ3-e42AoMuPw_-B3ISHvsvDroVpsIWM_f3vxY_r-JDBBeisUKHEe9IWkMQcSGHGhCsr9l3jCysiXO0gnvlQGr7lvGk-iLHzl0ZwP4acH8pV1w; _fbp=fb.1.1645524604989.230233926; adrdel=1; adrcid=ApHSD8WAyaOtJS914AUcB5w",
        "Host":"api.autoteka.ru",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0"
        }


class Parsing:
    def __init__(self, link):
        self.link = link
        self.check_link()
# https://autoteka.ru/report/web/uuid/a2f7fb8d-ff08-491a-a29f-652d500bcd44
# https://autoteka.ru/report/web/uuid/ce0c42af-5d30-49ba-83dd-9f49f14b714d
# \d-\d{3}-\d{3}-\d\d-\d\d tel number 8-888-888-88-88

    def check_link(self):
        temp = self.link.lower()
        pattern = "autoteka.ru/report/web/uuid/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
        match = re.search(pattern, temp)
        if match:
            pattern = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
            match = re.search(pattern, temp)
            self.link = "https://api.autoteka.ru/report/uuid/" + match.group() +".json?csAppCode=webDesktop"
        else:
            self.link = None
        pass

    def get_link(self):
        return self.link

    def parse(self):
        # define URL
        if self.link != None:
            # download data
            data = requests.get(url=self.link, headers=HEADER)
            dictionary = json.loads(data.text)

            with open('temp.json', 'w') as output_file:
                 output_file.write(data.text)


            print("vin_number : ", dictionary["head"]["vin"])
            # id
            # vin_number
            # goverment_number
            # body_number
            # engine_number
            # car_number
            # last_date
            # link
            # from_user



        # put in dataframe and clean-up
        # df = pd.DataFrame.from_dict(dictionary)
        # df = df.drop(range(6, 12), axis=1)
        pass

if __name__ == "__main__":
        # str = input("> :")
        # p = Parsing(str)
        # link = p.get_link()
        # if link != None:
        #     print(link)
        #     p.parse()


