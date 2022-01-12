class TikTakToe:

    def __init__(self):
        self.play_chr = (x for x in ['X', 'O', 'X', 'O', 'X', 'O', 'X', 'O', 'X', 'O'])
        # self.cells = cells.replace('_', ' ')
        # self.s = [[self.cells[0], self.cells[1], self.cells[2]],
        #     [self.cells[3], self.cells[4], self.cells[5]],
        #     [self.cells[6], self.cells[7], self.cells[8]]]
        self.s = [[' ', ' ', ' '],
                  [' ', ' ', ' '],
                  [' ', ' ', ' ']]
        self.user_chr = []
        self.x_count = 0
        self.o_count = 0
        self.x_win = 0
        self.o_win = 0
        self.msg = ''
        self.game()
        return

    def game(self):
        while True:
            self.user_in()
            self.check_win()
            if self.game_out() is False:
                break
        return

    def user_in(self):
        while True:
            user_step = input('Enter the coordinates: ')
            try:
                x, y = user_step.split()
                x = int(x)
                y = int(y)
                if user_step not in '3 1 1 2 2 1 3 3 2 3':
                    print('Coordinates should be from 1 to 3!')
                else:
                    if self.s[int(x) - 1][int(y) - 1] == ' ':
                        self.s[int(x) - 1][int(y) - 1] = next(self.play_chr)
                    else:
                        print('This cell is occupied! Choose another one!')
                        continue
                    break
            except TypeError:
                print('You should enter numbers!')
                continue

    def game_out(self):
        print('---------')
        for x in range(0, 3):
            print(f'| {self.s[x][0]} {self.s[x][1]} {self.s[x][2]} |')
        print('---------')
        if self.msg == 'Draw' or self.msg == 'X wins' or self.msg == 'O wins':
            print(self.msg)
            return False
        return

    def check_win(self):
        self.user_chr.clear()
        for i in range(3):
            self.user_chr.extend(self.s[i])
        self.o_count = self.user_chr.count('O')
        self.x_count = self.user_chr.count('X')
        dia = []
        if abs(self.o_count - self.x_count) > 1:
            print('Impossible1')
            return
        if self.o_count >= 3 or self.x_count >= 3 and abs(self.o_count - self.x_count) <= 1:
            # Diagonal 1
            for w in [0, 1, 2]:
                dia.append(self.s[w][w])
            if dia.count('X') == 3:
                self.x_win += 1
            if dia.count('O') == 3:
                self.o_win += 1
            dia = []
            # Diagonal 2
            for w, v in zip([0, 1, 2], [2, 1, 0]):
                dia.append(self.s[w][v])
            if dia.count('X') == 3:
                self.x_win += 1
            if dia.count('O') == 3:
                self.o_win += 1
            # Counts wins
            if self.s[0].count('X') == 3 or self.s[1].count('X') == 3 or self.s[2].count('X') == 3:
                self.x_win += 1
            if self.s[0].count('O') == 3 or self.s[1].count('O') == 3 or self.s[2].count('O') == 3:
                self.o_win += 1
            for i, j, k in zip(self.s[0], self.s[1], self.s[2]):
                if i == j == k in 'X':
                    self.x_win += 1
                if i == j == k in 'O':
                    self.o_win += 1
            if self.o_win == 1 and self.x_win == 1:
                print('Impossible2')
                return
            # Return Wins =============================================================================
            elif self.o_win == 0 and self.x_win == 0 and self.o_count + self.x_count == 9:
                self.msg = 'Draw'
                return
            elif self.x_win == 1:
                self.msg = 'X wins'
                return
            elif self.o_win == 1:
                self.msg = 'O wins'
                return
        else:
            return


game = TikTakToe()
