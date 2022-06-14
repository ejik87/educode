import os
import sys
from bs4 import BeautifulSoup
import requests
from colorama import Fore


def is_url_valid(url: str) -> bool:
    return "." in url


def url_to_filename(url: str) -> str:
    return url.rsplit(".", 1)[0].replace(".", "_")


class Browser:
    commands: set[str] = {"back", "exit"}
    cmd_history: list[str]
    tabs_dir: str

    def __init__(self, tabs_dir: str):
        self.cmd_history = []
        self.tabs_dir = tabs_dir

        if not os.path.exists(tabs_dir):
            os.makedirs(tabs_dir)

    def start(self) -> None:
        while True:
            self.cmd(input())
            print()

    def cmd(self, query: str, remember_history: bool = True) -> None:
        if query in self.commands:
            if query == "back":
                try:
                    self.cmd(self.cmd_history.pop(-2), remember_history=False)
                except IndexError:
                    print("Note: History is empty")
                finally:
                    return
            elif query == "exit":
                sys.exit()

        if is_url_valid(query):
            try:
                contents = self.request_contents(query)
            except requests.exceptions.ConnectionError:
                print("Error: Incorrect URL")
            else:
                print(contents)
                self.save_contents(query, contents)
        else:
            try:
                contents = self.retrieve_contents(query)
            except FileNotFoundError:
                print("Error: Incorrect URL")
            else:
                print(contents)
            finally:
                if remember_history:
                    self.cmd_history.append(query)

    def retrieve_contents(self, url: str) -> str:
        path = os.path.join(self.tabs_dir, url_to_filename(url))
        with open(path) as f:
            return f.read()

    def save_contents(self, url: str, contents: str) -> None:
        path = os.path.join(self.tabs_dir, url_to_filename(url))
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(contents)

    @staticmethod
    def request_contents(url: str) -> str:
        url = url if url.startswith("http") else f"https://{url}"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        # return requests.get(url, headers={"User-Agent": user_agent}).text
        page = requests.get(url, headers={"User-Agent": user_agent}).text
        soup = BeautifulSoup(page, 'html.parser')

        for tag in soup.find_all("a"):
            if tag.get_text():
                tag.string = '\033[34m' + tag.get_text() + '\033[39m'

        return soup.get_text()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Wrong number of arguments. Did you specify the tabs folder?")
    else:
        b = Browser(sys.argv[1])

    b.start()
