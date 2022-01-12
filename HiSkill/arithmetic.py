import random


class Exam:
    intro = ['Which level do you want? Enter a number:', '1 - simple operations with numbers 2-9',
             '2 - integral squares of 11-29']

    def __init__(self):
        self.r_gen = ''
        self.u_enter = ''
        self.count = 0
        self.answers = 0
        self.level = 1
        self.main()

    def main(self):
        while True:
            print(*self.intro, sep='\n')
            self.level = input()
            if self.level in ['1', '2']:
                if self.level == '1':
                    self.check(1)
                    break
                elif self.level == '2':
                    self.check(2)
                    break
            else:
                print('Incorrect format.')
                continue

    def check(self, n):
        while self.count < 5:
            self.r_gen = self.gen(n)
            print(self.r_gen)
            while True:
                try:
                    self.u_enter = int(input())
                    break
                except (ValueError, TypeError):
                    print('Incorrect format.')
                    continue
            if self.u_enter == self.calc(self.r_gen):
                self.answers += 1
                print('Right!')
                self.count += 1
                continue
            else:
                print('Wrong!')
                self.count += 1
                continue
        print(f'Your mark is {self.answers}/{self.count}. Would you like to save the result? Enter yes or no.')
        ask = input()
        if ask.lower() in ['yes', 'y']:
            with open('results.txt', 'a', encoding='UTF-8') as file_txt:
                u_name = input('What is your name?')
                file_txt.writelines(f'{u_name}: {self.answers}/{self.count} in level {self.level} ({self.intro[int(self.level)][4:]}).')
                print('The results are saved in "results.txt".')
        else:
            return

    def gen(self, level):
        if level == 1:
            r_gen = f'{random.randint(2, 9)} {random.choice(["+", "-", "*"])} {random.randint(2, 9)}'
            return r_gen
        elif level == 2:
            r_gen = random.randint(11, 29)
            return r_gen

    def calc(self, num):
        if self.level == '1':
            a, o, b = num.split()
            arithmetic = {"*": lambda x, y: x * y,
                          "+": lambda x, y: x + y,
                          "-": lambda x, y: x - y}

            return arithmetic[o](int(a), int(b))
        if self.level == '2':
            return pow(int(num), 2)


execute = Exam()
