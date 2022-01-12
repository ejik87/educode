help_msg = "Available formatters: plain bold italic header link inline-code ordered-list unordered-list new-line\
\nSpecial commands: !help !done"
err_msg = "Unknown formatting type or command"

avalible_cmd = [
    'plain',
    'bold',
    'italic',
    'inline_code',
    'link',
    'header',
    'unordered_list',
    'ordered_list',
    'new_line',
    'line_break'
]

text_out = []


def decor(func):  # replace - to _ for run function by name.
    def wrapper(args):
        arg = args.replace('-', '_')
        # print(arg)
        func(arg)

    return wrapper


@decor
def chk_enter(txt):
    if str(txt) == '!help':
        print(help_msg)
    elif str(txt) == '!done':
        f = open('output.md', 'w', encoding='UTF-8')
        f.write(''.join(text_out))
        f.close()
        exit()
    elif txt in avalible_cmd:
        func_run(globals()[txt])
        return
    else:
        print(err_msg)


def func_run(func):
    return func()


def plain():
    text_out.append(str(input('Text: ')))


def italic():
    text_out.append(str(f"*{input('Text: ')}*"))


def bold():
    text_out.append(str(f"**{input('Text: ')}**"))


def header():
    while True:
        lvl = int(input('Level: '))
        if 1 <= lvl <= 6:
            text_out.append(str(f"{r'#' * lvl} {input('Text: ')}\n"))
            break
        else:
            print('The level should be within the range of 1 to 6')
            continue


def link():
    lbl = str(input('Label: '))
    text_out.append(str(f"[{lbl}]({input('URL: ')})"))


def inline_code():
    text_out.append(str(f"`{input('Text: ')}`"))


def new_line():
    text_out.append(str("\n"))


def line_break():
    text_out.append(str("\n"))


def ordered_list():
    while True:
        rows = int(input('Number of rows: '))
        if rows > 0:
            for i in range(1, rows + 1):
                text_out.append(str(f'{i}. {input(f"Row #{i}: ")}\n'))
            break
        else:
            print("The number of rows should be greater than zero")
            continue


def unordered_list():
    while True:
        rows = int(input('Number of rows: '))
        if rows > 0:
            for i in range(1, rows + 1):
                text_out.append(str(f'* {input(f"Row #{i}: ")}\n'))
            break
        else:
            print("The number of rows should be greater than zero")
            continue


while True:
    _text = input("Choose a formatter: ")
    chk_enter(_text)
    print(''.join(text_out))
    continue
