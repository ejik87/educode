import random

# actions if user win!
def user_win():
    print(f'Well done. The computer chose {bot_var} and failed')
    global score
    score += 100
    return score

# actions if draw
def user_draw():
    print(f'There is a draw ({bot_var})')
    global score
    score += 50
    return score

# actions if user loose.
def user_loose():
    return print(f'Sorry, but the computer chose {bot_var}')


# Add user variable hand.
def user_rules(x):
    global game
    global ext_game
    list_x = x.split(',')
    for k, v in ext_game.items():
        if k in list_x:
            game[k] = v
    print('Okay, let\'s start')


# Start programm.
enter_user = input('Enter your name: ')
file_base = open('/Users/ej/Projects/edu/rating.txt', 'r+', encoding='utf-8')

for name in file_base:
    read_list = name.rstrip().split()
    if read_list[0] == enter_user:
        user_name = read_list[0]
        score = int(read_list[1])
        break
    else:
        user_name = enter_user
        score = 0
print(f'Hello, {enter_user} !')

# Enter rules game
user_opt_game = input()

std_game = {
    'rock': 'paper',
    'scissors': 'rock',
    'paper': 'scissors'
}

ext_game = {
    'rock': ['paper', 'air', 'water', 'dragon', 'devil', 'lightning', 'gun'],
    'scissors': ['rock', 'fire', 'water', 'dragon', 'devil', 'lightning', 'gun'],
    'paper': ['scissors', 'sponge', 'wolf', 'tree', 'human', 'snake', 'fire'],
    'gun': ['sponge', 'paper', 'air', 'water', 'dragon', 'devil', 'lightning'],
    'water': ['human', 'snake' 'tree', 'wolf', 'sponge', 'paper', 'air'],
    'fire': ['rock', 'air', 'water', 'dragon', 'devil', 'lightning', 'gun'],
    'snake': ['rock', 'fire', 'scissors', 'dragon', 'devil', 'lightning', 'gun'],
    'human': ['rock', 'fire', 'scissors', 'snake', 'devil', 'lightning', 'gun'],
    'tree': ['rock', 'fire', 'scissors', 'snake', 'human', 'lightning', 'gun'],
    'wolf': ['rock', 'fire', 'scissors', 'snake', 'human', 'tree', 'gun'],
    'sponge': ['rock', 'fire', 'scissors', 'snake', 'human', 'tree', 'wolf'],
    'air': ['scissors', 'snake', 'human', 'tree', 'wolf', 'sponge', 'paper'],
    'dragon': ['human', 'tree', 'wolf', 'sponge', 'paper', 'air', 'water'],
    'devil': ['tree', 'wolf', 'sponge', 'paper', 'air', 'water', 'dragon'],
    'lightning': ['wolf', 'sponge', 'paper', 'air', 'water', 'dragon', 'devil']
}

game = {}


# Change rule game
if user_opt_game == '':
    game = std_game
    print('Okay, let\'s start')
elif user_opt_game:
    user_rules(user_opt_game)


while True:
    user_var = input()
    bot_var = random.choice(list(game.keys()))
    if user_var == '!exit':
        print('Bye!')
        file_base.close()
        break
    elif user_var == '!rating':
        print(f'Your rating: {score}')
        continue
    elif user_var not in list(game.keys()):
        print('Invalid input')
        continue
    elif user_var == bot_var:
        user_draw()
        continue
    else:
        if bot_var in game[user_var]:
            user_loose()
            continue
        else:
            user_win()
            continue
