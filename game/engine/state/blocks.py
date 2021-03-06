from operator import itemgetter
from random import randint
from settings import settings
from utils import Cell, Position
from key_bindings import User_Input
from math import sin, cos


# Abstract class laying groundwork for each type of block in the game
class Block:
    # Initialize key properties used by this class and by child classes
    def __init__(self, color):
        self.base_position = Position(settings.new_block_position.x, settings.new_block_position.y)
        self.color = color

    # Set block's new position
    def set_cells(self, cells):
        self.cells = cells

    def calculate_new_cells(self, user_input):
        # CZY TU I NIŻEJ NIE BĘDZIE PROBLEMÓW ŻE IN-PLACE?
        # JAK TO ZOPTYMALIZOWAĆ?
        for cell in self.cells:
            x = cell.position.x
            y = cell.position.y
            if user_input == User_Input.MOVE_LEFT:
                cell.position = Position(x, y - 1)
            if user_input == User_Input.MOVE_RIGHT:
                cell.position = Position(x, y + 1)
            if user_input == User_Input.MOVE_DOWN:
                cell.position = Position(x + 1, y)
            else:
                break
        if user_input == User_Input.ROTATE:
            self._rotate()
        return self.cells

    #
    def _rotate(self, rotation):
        for cell in self.cells:
            x = cell.position.x
            y = cell.position.y
            x_ = x*cos(rotation) - y*sin(rotation)
            y_ = y*cos(rotation) + x*sin(rotation)
            # IN PLACE?
            cell.position = Position(round(x_), round(y_))

class Square_Block(Block):
    # I CO Z TEGO, ŻE MISSED?
    def __init__(self):
        super.__init__()
        x, y = itemgetter('x', 'y')(self.base_position)
        self.cells = [
            Cell(x - 1, y - 1, self.color),
            Cell(x, y - 1, self.color),
            Cell(x - 1, y, self.color),
            Cell(x, y, self.color)
        ]

    # Overwrite default _rotate method to prevent rotation    
    def _rotate(self):
        return self.cells


class L_Block(Block):
    def __init__(self):
        super.__init__()
        x, y = itemgetter('x', 'y')(self.base_position)
        self.cells = [
            Cell(x + 1, y - 1, self.color),
            Cell(x - 1, y, self.color),
            Cell(x, y, self.color),
            Cell(x + 1, y, self.color)
        ]

class L_Mirror_Block(Block):
    def __init__(self):
        super.__init__()
        x, y = itemgetter('x', 'y')(self.base_position)
        self.cells = [
            Cell(x - 1, y, self.color),
            Cell(x, y, self.color),
            Cell(x + 1, y, self.color),
            Cell(x + 1, y + 1, self.color)
        ]

class Line_Block(Block):
    def __init__(self):
        super.__init__()
        x, y = itemgetter('x', 'y')(self.base_position)
        self.cells = [
            Cell(x - 1, y, self.color),
            Cell(x, y, self.color),
            Cell(x + 1, y, self.color)
        ]

class Diagonal_Block(Block):
    def __init__(self):
        super.__init__()
        x, y = itemgetter('x', 'y')(self.base_position)
        self.cells = [
            Cell(x - 1, y - 1, self.color),
            Cell(x, y - 1, self.color),
            Cell(x, y, self.color),
            Cell(x + 1, y, self.color)
        ]

class Diagonal_Mirror_Block(Block):
    def __init__(self):
        super.__init__()
        x, y = itemgetter('x', 'y')(self.base_position)
        self.cells = [
            Cell(x - 1, y + 1, self.color),
            Cell(x, y + 1, self.color),
            Cell(x, y, self.color),
            Cell(x + 1, y, self.color)
        ]

class Spaceship_Block(Block):
    def __init__(self):
        super.__init__()
        x, y = itemgetter('x', 'y')(self.base_position)
        self.cells = [
            Cell(x, y - 1, self.color),
            Cell(x - 1, y, self.color),
            Cell(x, y, self.color),
            Cell(x + 1, y, self.color)
        ]


def create_random_block():
    # PRZENIESC LISTE DOSTEPNYCH TYPOW KLOCKOW DO SETTINGS
    block_types = [Square_Block, L_Block, L_Mirror_Block, Line_Block, Diagonal_Block, Diagonal_Mirror_Block, Spaceship_Block]
    color = settings.colors[randint(0, settings.colors.__len__())]
    block_type = block_types[randint(0, block_types.__len__())]
    return block_type(color)