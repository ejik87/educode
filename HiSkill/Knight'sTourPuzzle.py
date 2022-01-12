import copy

leave_horse = [[2, 1], [-2, 1], [2, -1], [-2, -1], [1, 2], [-1, 2], [1, -2], [-1, -2]]
board = []
show_board = []
auto_board = []
cell_size = 1
posbl_cell = []  # memory possible cells and check movie
x_in = 0
y_in = 0
column_n = 0
row_n = 0
posbl_mov = bool()  # Flag
sqr_count = 0  # squares count


def build_board(column, row):
    for y in range(row):
        board.append([])
        for x in range(column):
            board[y].append(f'{cell_size * "_"}')


def poss():
    global leave_horse
    global x_in
    global y_in
    global column_n
    global row_n
    global sqr_count
    global posbl_mov
    global posbl_cell
    global show_board

    posbl_cell.clear()
    for x, y in leave_horse:
        x += x_in
        y += y_in
        if x in range(1, column_n + 1):
            if y in range(1, row_n + 1):
                if '*' not in board[y - 1][x - 1]:
                    chk = poss_next(x, y)
                    if chk is not None:
                        show_board[y - 1][x - 1] = str(chk).rjust(cell_size)
                        posbl_cell.append([x, y])
                    else:
                        pass


def poss_next(x_2, y_2):
    global leave_horse
    global x_in
    global y_in
    global column_n
    global row_n
    global sqr_count
    global posbl_mov

    count = 0
    for x, y in leave_horse:
        x += x_2
        y += y_2
        if x == x_in and y == y_in:
            continue
        elif x in range(1, column_n + 1):
            if y in range(1, row_n + 1):
                count += 1
    if count > 0:
        return count
    return


def auto_horse(_board, next_x, next_y, count):
    # This is greate loop func! So hard to understand!
    global column_n
    global row_n
    global auto_board
    global sqr_count

    for n in range(len(leave_horse)):
        if count >= (column_n * row_n) + 1:
            sqr_count = count
            return True
        x = leave_horse[n][0] + next_x
        y = leave_horse[n][1] + next_y
        if check_position(x, y) and check_place(_board, x, y):
            _board[y - 1][x - 1] = str(count).rjust(cell_size)
            if auto_horse(_board, x, y, count + 1):
                return True
            _board[y - 1][x - 1] = f'{cell_size * "_"}'
    return False


def print_board(board_in):
    global cell_size
    global column_n
    global row_n

    print(f'{" " * len(str(row_n))}{(column_n * (cell_size + 1) + 3) * "-"}')  # Рисуем -------- сверху.
    for n, s in zip(range(row_n, 0, -1), board_in[::-1]):
        print(f'{str(n).rjust(len(str(row_n)))}| {" ".join(s)} |')  # Рисуем содержимое поля из листа.
    print(f'{" " * len(str(row_n))}{(column_n * (cell_size + 1) + 3) * "-"}\n  ', end='')  # Рисуем -------- снизу.
    for b in range(1, column_n + 1):
        print(f' {str(b).rjust(cell_size)}', end='')


def out():
    global board
    global cell_size
    global posbl_cell
    global x_in
    global y_in
    global show_board
    global posbl_mov
    global sqr_count

    show_board.clear()
    show_board = copy.deepcopy(board)
    poss()
    show_board[y_in - 1][x_in - 1] = 'X'.rjust(cell_size)
    print_board(show_board)
    print('\n')
    board[y_in - 1][x_in - 1] = '*'.rjust(cell_size)
    sqr_count += 1
    if posbl_cell:
        posbl_mov = True
    else:
        posbl_mov = False


def start_horse():
    global board
    global auto_board
    global cell_size
    global x_in
    global y_in
    global column_n
    global row_n
    global sqr_count
    while True:
        try:
            column_n, row_n = map(int, input("Enter your board dimensions:").split())
            if 0 < column_n and 0 < row_n:
                break
            else:
                raise TypeError
        except (TypeError, ValueError):
            print('Invalid move! ', end='')
            continue
    cell_size = len(str(column_n * row_n))

    while True:
        try:
            x_in, y_in = map(int, input("Enter the knight's starting position: ").split())
            if check_position(x_in, y_in):
                build_board(column_n, row_n)  # Build Board and mark position.
                break
            else:
                raise TypeError
        except (TypeError, ValueError):
            print('Invalid move! ', end='')
            continue
    while True:
        try:
            m_o_a = input("Do you want to try the puzzle? (y/n): ").lower()
            if m_o_a in 'yn':
                if m_o_a == 'y':
                    auto_board = copy.deepcopy(board)
                    auto_board[y_in - 1][x_in - 1] = '1'.rjust(cell_size)
                    auto_horse(auto_board, x_in, y_in, 2)
                    if sqr_count == (column_n * row_n) + 1:
                        out()
                        sqr_count = 1
                        loop_horse()
                    else:
                        print("No solution exists!")
                        exit()
                if m_o_a == 'n':
                    auto_board = copy.deepcopy(board)
                    auto_board[y_in - 1][x_in - 1] = '1'.rjust(cell_size)
                    auto_horse(auto_board, x_in, y_in, 2)
                    if sqr_count == (column_n * row_n) + 1:
                        print("\nHere's the solution!")
                        print_board(auto_board)
                        exit()
                    else:
                        print("No solution exists!")
                        exit()
            else:
                raise TypeError
        except (TypeError, ValueError):
            print('Invalid move! ', end='')
            continue


def loop_horse():
    global board
    global cell_size
    global posbl_cell
    global x_in
    global y_in
    global column_n
    global row_n
    global sqr_count
    global posbl_mov

    while True:
        if not posbl_mov:
            if sqr_count == (column_n * row_n):
                print('What a great tour! Congratulations!')
            else:
                print(f'No more possible moves!\nYour knight visited {sqr_count} squares!')
            exit()
        else:
            try:
                x_in, y_in = map(int, input("Enter your next move: ").split())
                if check_position(x_in, y_in) and check_place(board, x_in, y_in) and chk_l_sqr(x_in, y_in):
                    out()
                    continue
                else:
                    raise TypeError
            except (TypeError, ValueError):
                print('Invalid move! ', end='')


def chk_l_sqr(col, row):  # Check L-type square.
    for chk_xy in posbl_cell:
        if chk_xy == [col, row]:
            return True


def check_position(col, row):  # New function check horse to cell ================================================
    if 0 < col <= column_n and 0 < row <= row_n:
        return True


def check_place(_board, col, row):  # Check free spase to square.
    if '_' in _board[row - 1][col - 1]:
        return True


def main():
    global board

    if row_n:
        loop_horse()
    else:
        start_horse()


while True:
    try:
        main()

    except (TypeError, ValueError):
        print('Invalid move! Enter your next move: ')
        continue
