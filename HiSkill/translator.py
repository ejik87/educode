import requests
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="This program prints translates. Exemple:\
    <Enter language> <Destination language or All> <Word to translate>.")
parser.add_argument("enter_lang")
parser.add_argument("dest_lang")
parser.add_argument("word")


class Translater:
    headers = {'User-Agent': 'Mozilla/5.0'}
    lang_var = ['arabic', 'german', 'english', 'spanish', 'french', 'hebrew', 'japanese', 'dutch', 'polish',
                'portuguese', 'romanian', 'russian', 'turkish', 'all']

    def __init__(self):
        self.args = parser.parse_args()
        self.file_var = ''
        self.lang_enter = self.args.enter_lang  # Язык ввода.
        self.lang_dest = self.args.dest_lang  # Язык для перевода.
        self.word = self.args.word
        self.web = 'https://context.reverso.net/translation/'
        self.url = ''
        if self.lang_dest not in self.lang_var:
            print(f"Sorry, the program doesn't support {self.lang_dest}")
            return
        elif self.lang_enter not in self.lang_var:
            print(f"Sorry, the program doesn't support {self.lang_enter}")
            return
        if self.lang_dest == 'all':
            for i in range(0, 13):  # Circle all lang.
                self.main(self.lang_var[i])
        else:
            self.main(self.lang_dest)

        with open(f'{self.word}.txt', 'w', encoding='UTF-8') as self.word_txt:
            self.word_txt.write(self.file_var)

    def main(self, lang):
        if lang == self.lang_enter:
            return
        self.build_url(lang)
        self.translate_get(lang)

    def build_url(self, lang):
        self.url = ''
        self.url = self.web + self.lang_enter + '-' + lang + '/' + self.word
        self.page = requests.get(self.url, headers=self.headers)
        if self.page:  # Check respond
            pass
        else:
            print('Something wrong with your internet connection')
            return

    def translate_get(self, lang):
        out_lang = lang.capitalize()
        soup = BeautifulSoup(self.page.content, 'html.parser')
        no_result = soup.select('#no-results > .wide-container')
        for no_r in no_result:
            temp1 = no_r.text.strip()
            if self.word in temp1:
                print(f'Sorry, unable to find {self.word}')
                return
        example_text = soup.find("section", {"id": "examples-content"}).find_all("span", {"class": "text"})
        translated = [x.text.strip() for x in soup.select("#translations-content > .translation")]
        examples = []
        for e in example_text:
            if len(examples) < 10:
                examples.append(e.text.strip())
            else:
                break
        if self.lang_dest == 'all':
            self.file_var += f'\n{out_lang} Translations:\n'
            print('\n' + out_lang, 'Translations:')
            self.file_var += (translated[0] + '\n')
            print(translated[0])
            self.file_var += f'\n{out_lang} Examples:\n'
            print('\n' + out_lang, 'Examples:')
            self.file_var += f'{examples[0]}:\n{examples[1]}\n'
            print(f'{examples[0]}:\n{examples[1]}')
        else:
            self.file_var += f'\n{out_lang} Translations:\n'
            print('\n' + out_lang, 'Translations:')
            for j in range(5):
                self.file_var += f'{translated[j]}\n'
                print(translated[j])
            self.file_var += f'\n{out_lang} Examples:\n'
            print('\n' + out_lang, 'Examples:')
            for i in range(0, 10, 2):
                self.file_var += f'{examples[i]}:\n{examples[i+1]}\n\n'
                print(f'{examples[i]}:\n{examples[i+1]}\n')


if __name__ == '__main__':
    run = Translater()
