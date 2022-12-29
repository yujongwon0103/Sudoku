import numpy as np
from collections import Counter


class SudokuException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def init_sudoku():
    print("Let's play Sudoku!")
    while True:
        try:
            size = int(input("\rPlease enter the sudoku size! ONLY square number! Recommended maximum 16! : "))
            if size <= 0:
                raise SudokuException("MUST be greater than ZERO!")
            elif size > 0 and np.sqrt(size) % 1 != 0:
                raise SudokuException("SQUARE NUMBER ONLY")
        except ValueError:
            print("NUMBER ONLY!")
        except Exception as e:
            print(str(e))
        else:
            while True:
                try:
                    diff = input("Refer to the following example, Please enter the sudoku difficulty level!\n["
                                 "Easy, Normal, Hard, Expert, Evil] : ")
                    if diff not in ["Easy", "Normal", "Hard", "Expert", "Evil"]:
                        raise SudokuException("Wrong level!")
                except Exception as e:
                    print(str(e))
                else:
                    return size, diff


def check_duplication(li):
    for i in li:
        for j in i:
            if len([item for item, count in Counter(j).items() if count > 1]) > 0:
                return False
    return True


class Sudoku:
    def __init__(self):
        self.size, self.diff = init_sudoku()
        self.square = int(np.sqrt(self.size))
        self.nums = np.arange(1, self.size + 1)
        self.board = np.zeros(shape=(self.size, self.size))
        self.difficulty = {"Easy": np.arange(round(self.size**2 * 0.5), round(self.size**2 * 0.55)),
                           "Normal": np.arange(round(self.size**2 * 0.55), round(self.size**2 * 0.6)),
                           "Hard": np.arange(round(self.size**2 * 0.6), round(self.size**2 * 0.65)),
                           "Expert": np.arange(round(self.size**2 * 0.65), round(self.size**2 * 0.7)),
                           "Evil": np.arange(round(self.size**2 * 0.7), round(self.size**2 * 0.75))}
        self.hidden_count = self.size if self.size == 1 else np.random.choice(self.difficulty[self.diff], 1)[0]
        self.generate_board()
        self.board_copy = self.board.copy()
        self.setting_difficulty()
        self.show_board()
        self.play_sudoku()

    def generate_board(self):
        i = 0
        j = 0
        while i < self.size:
            x = (i // self.square) * self.square
            while j < self.size:
                y = (j // self.square) * self.square
                row = self.board[i, :j]
                col = self.board[:i, j]
                arr = self.board[x: x + self.square, y: y + self.square]

                usable_nums = np.setdiff1d(self.nums, np.union1d(np.union1d(row, col), arr[np.where(arr > 0)]))

                if len(usable_nums) > 0:
                    self.board[i][j] = np.random.choice(usable_nums, 1, replace=False)
                    j += 1
                else:
                    self.board[x:i+1] = np.zeros(shape=(i-x+1, self.size))
                    i = x
                    j = 0
            i += 1
            j = 0
        if not self.check_requirement():
            self.generate_board()

    def check_all_num(self, li):
        for i in li:
            for j in i:
                if (np.unique(j) != self.nums).any():
                    return False
        return True

    def check_requirement(self):
        row = self.board
        col = self.board.T
        arr_li = np.hsplit(self.board, self.square)
        arr = arr_li[0]
        for i in range(len(arr_li)):
            if i + 1 < len(arr_li):
                arr = np.concatenate([arr, arr_li[i+1]])
        arr = arr.reshape(self.size, self.size)
        return True if self.check_all_num([row, col, arr]) & check_duplication([row, col, arr]) else False

    def setting_difficulty(self):
        k = 0
        while k < self.hidden_count:
            i, j = np.random.choice(np.arange(self.size), 2)
            if self.board_copy[i][j] != 0:
                self.board_copy[i][j] = 0
                k += 1

    def create_line(self, s, first, middle, end):
        s += first
        for _ in range(self.square):
            s += "━" * ((len(str(self.size))+1) * self.square + 1) + middle
        s = s[:-1] + end + "\n"
        return s

    def show_board(self):
        max_word_len = len(str(self.size))
        s = " " * max_word_len + "  "
        for j in range(1, self.size + 1):
            s += " " * (max_word_len - len(str(j))) + str(j) + " "
            if j % self.square == 0:
                s += "  "
        s = s[:-1] + "\n"
        for i in range(self.size + self.square + 1):
            if i % (self.square+1) == 0:
                if i == 0:
                    s = self.create_line(s, " " * max_word_len + "┏", "┳", "┓")
                elif i == self.size + self.square:
                    s = self.create_line(s, " " * max_word_len + "┗", "┻", "┛")
                else:
                    s = self.create_line(s, " " * max_word_len + "┣", "╋", "┫")
            else:
                x = i // (self.square + 1) * self.square + i % (self.square + 1) - 1
                s += " " * (max_word_len - len(str(x+1))) + str(x+1)
                for a in range(self.square):
                    s += "┃ "
                    for b in range(self.square):
                        y = a * self.square + b
                        num = int(self.board_copy[x][y])
                        if num == 0:
                            s += " " * (max_word_len + 1)
                        else:
                            s += " " * (max_word_len - len(str(num))) + str(num) + " "
                s += "┃\n"
        print(s[:-1])

    def play_sudoku(self):
        while self.hidden_count != 0:
            try:
                x, y, ans = input("\rPlease enter the sudoku's x, y coordinates and answer (ex. 1 2 3) : ").split()
                if self.board[int(x)-1][int(y)-1] == int(ans):
                    print("Correct answer!")
                    self.board_copy[int(x)-1][int(y)-1] = int(ans)
                    self.hidden_count -= 1
                else:
                    print("Wrong answer!")
                self.show_board()
            except ValueError:
                print("NUMBER ONLY!")
            except Exception as e:
                print(str(e))
        print("Congratulation!")


if __name__ == '__main__':
    sudoku = Sudoku()
