import math
from operator import itemgetter

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Cell:
    def __init__(self, x, y, color):
        self.position = Position(x,y)
        self.color = color

class Test_Block:
    def __init__(self):
        color = 'red'
        x = 0
        y = 0
        self.rotation = 0
        self.cells = [
            Cell(x + 1, y - 1, color),
            Cell(x - 1, y, color),
            Cell(x, y, color),
            Cell(x + 1, y, color)
        ]
    def _rotate(self, rotation):
        self.rotation += rotation
        for cell in self.cells:
            x = cell.position.x
            y = cell.position.y
            x_ = x*math.cos(self.rotation) - y*math.sin(self.rotation)
            y_ = y*math.cos(self.rotation) + x*math.sin(self.rotation)
            # IN PLACE?
            cell.position = Position(int(x_), int(y_))
            print('***CELL***')
            print(f'x: {int(x_)}; y: {int(y_)}')
            print('**********')
        return self.cells



def rotate_and_print(rotation):
    block = Test_Block()
    cells = block._rotate(rotation)
    board = [[False, False, False], [False, False, False], [False, False, False]]
    for cell in cells:
        board[cell.position.x + 1][cell.position.y + 1] = True
    for row in board:
        row_s = ''
        for column in row:
            if column:
                row_s += 'X\t'
            else:
                row_s += '.\t'
        print (row_s)
        print('__________________')
    print('||||||||||||||||||')

rotate_and_print(0)
rotate_and_print(math.pi/2)
