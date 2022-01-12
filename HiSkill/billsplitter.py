import  random

count = int(input('Enter the number of friends joining (including you):\n'))

if count > 0:
    names = []
    i = 0
    print('\nEnter the name of every friend (including you), each on a new line:')
    while i < count:
        names.append(input())
        i += 1
    sb_dict = dict.fromkeys(names, 0)

    split = input('\nEnter the total bill value:\n')

    if input('\nDo you want to use the "Who is lucky?" feature? Write Yes/No:\n').lower() == 'yes':
        lucky = random.choice(list(sb_dict))
        print(f'\n{lucky} is the lucky one!')
        for i in sb_dict:
            sb_dict[i] = round(float(split)/(count - 1), 2)
        sb_dict[lucky] = 0

    else:
        print('\nNo one is going to be lucky')
        for i in sb_dict:
            sb_dict[i] = round(float(split) / count, 2)
    print(sb_dict)
else:
    print('No one is joining for the party')

#except (ValueError, TypeError):
#    print('No one is joining for the party')


