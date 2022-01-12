import random
words = ['python', 'java', 'kotlin', 'javascript']
print('H A N G M A N')

def main():
    random_word = random.choice(words)
    gues = {}
    for i, j in enumerate(random_word):
        gues.setdefault(i, '-')
    count = 8
    _print = ''
    chanse = []
    while count >= 1:
        _print = (''.join(gues.values()))
        print('\n' + _print)
        if random_word == _print:
            print(f"You guessed the word {random_word}!\nYou survived!")
            exit()
        else:
            user_word = input(f'Input a letter:')
            if len(user_word) > 1:
                print('You should input a single letter')
                continue
            if user_word.islower() and user_word.isalpha():
                if user_word in chanse:
                    print("You've already guessed this letter")
                    continue
                if user_word in random_word and user_word:
                    chanse.append(user_word)
                    for num, w in enumerate(random_word):
                        if user_word == w:
                            gues[num] = user_word
                else:
                    chanse.append(user_word)
                    count -= 1
                    print("That letter doesn't appear in the word")
                    continue
            else:
                print('Please enter a lowercase English letter')
    print("You lost!")

while True:
    print('Type "play" to play the game, "exit" to quit:')
    comd = input()
    if comd in ['play', 'exit']:
        if comd == 'play':
            main()
            continue
        elif comd == 'exit':
            break
        else:
            continue
