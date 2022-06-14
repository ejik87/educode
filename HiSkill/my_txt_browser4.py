import os
import argparse
from collections import deque
import requests
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="This program prints Web from entering url.")
parser.add_argument("path_cache", help='Enter path to cache dir.')

nytimes_com = '''
This New Liquid Is Magnetic, and Mesmerizing

Scientists have created “soft” magnets that can flow 
and change shape, and that could be a boon to medicine 
and robotics. (Source: New York Times)


Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

Jessica Wade has added nearly 700 Wikipedia biographies for
 important female and minority scientists in less than two 
 years.

'''

bloomberg_com = '''
The Space Race: From Apollo 11 to Elon Musk

It's 50 years since the world was gripped by historic images
 of Apollo 11, and Neil Armstrong -- the first man to walk 
 on the moon. It was the height of the Cold War, and the charts
 were filled with David Bowie's Space Oddity, and Creedence's 
 Bad Moon Rising. The world is a very different place than 
 it was 5 decades ago. But how has the space race changed since
 the summer of '69? (Source: Bloomberg)


Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

Twitter and Square Chief Executive Officer Jack Dorsey 
 addressed Apple Inc. employees at the iPhone maker’s headquarters
 Tuesday, a signal of the strong ties between the Silicon Valley giants.
'''

urls = {'nytimes.com': nytimes_com, 'bloomberg.com': bloomberg_com}


class CmdBrowser:

    def __init__(self):
        self.args = parser.parse_args()
        self.url = ''
        self.web = 'https://'
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.path_cache = self.args.path_cache  # Выбираем отдельный аргумент
        self.cache_list = []
        self.history = deque()
        self.page = None

        if not os.access(self.path_cache, os.F_OK):  # Проверяем есть ли такой каталог
            os.makedirs(self.path_cache)  # создаём, если нет

    def check_cache(self, url):
        cache_name = url.split(".", -1)[0]  # очищаем запрос от последней точки и то что за ней
        if cache_name in self.cache_list:
            self.read_cache(url)
        else:
            self.add_cache(url)

    def add_cache(self, url):
        cache_name = url.split(".", -1)[0]  # очищаем запрос от последней точки и то что за ней
        self.cache_list = list(os.listdir(self.path_cache))

        with open(f'{self.path_cache}/{cache_name}', 'w', encoding="UTF-8") as cf:
            cf.write(self.web_request(url))
            cf.flush()

    def read_cache(self, request):
        cache_name = request.rsplit(".", 1)[0]  # очищаем запрос от последней точки и то что за ней
        self.cache_list = list(os.listdir(self.path_cache))
        if cache_name in self.cache_list:
            with open(f'{self.path_cache}/{cache_name}', 'r', encoding="UTF-8") as cf:
                return cf.readlines()
        else:
            print('Error: Incorrect URL')

    def web_request(self, request):
        web_url = self.web + request
        self.page = requests.get(web_url, headers=self.headers)
        #self.page = BeautifulSoup(page.content, 'html.parser')
        if self.page:  # Check respond
            return self.page.text
        else:
            print('Something wrong with your internet connection')
            return

    def run(self):
        while True:
            self.url = input()
            if self.url == 'exit':
                break
            elif self.url == 'back':
                if len(self.history) > 1:
                    self.history.pop()
                    self.url = self.history[-1]
                    print(self.read_cache(self.url))
                    # print(urls[self.url])  # old
                else:
                    continue
            # elif self.url in urls:
            #     self.check_cache(self.url)
            #     print(urls[self.url])
            #     self.history.append(self.url)
            else:  # Если ссылка
                self.check_cache(self.url)
                # print(self.read_cache(self.url))
                print(self.page.text)
                self.history.append(self.url)
            # else:
            #     self.read_cache(self.url)


browser = CmdBrowser()
browser.run()
