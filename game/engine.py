from enum import Enum

from settings import settings

# Helper class for keeping track of cells' coordinates
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Cell:
    def __init__(self, x, y, color):
        self.position = Position(x,y)
        self.color = color

class User_Input(Enum):
    MOVE_LEFT = 'l'
    MOVE_RIGHT = 'r'
    MOVE_DOWN = 'd'
    ROTATE = 'r'




# Abstract class laying groundwork for each type of block in the game
class Block:
    # Initialize key properties used by this class and by child classes
    def __init__(self):
        raise NotImplementedError('Objects should never be created from Block class. Use descendant classes instead.')
        # DODAĆ TWORZENIE NOWEGO KLOCKA (WYPEŁNIANIE CELLS)

    # Set block's new position
    def set_cells(self, cells):
        self.cells = cells

    def calculate_move(self, user_input):
        # CZY TU I NIŻEJ NIE BĘDZIE PROBLEMÓW ŻE IN-PLACE?
        # JAK TO ZOPTYMALIZOWAĆ?
        for cell in self.cells:
            x = cell.position.x
            y = cell.position.y
            if user_input == User_Input.MOVE_LEFT:
                cell.position = Position(x, y - 1)
            if user_input == User_Input.MOVE_RIGHT:
                cell.position = Position(x, y + 1)
            if user_input == User_Input.MOVE_RIGHT:
                cell.position = Position(x + 1, y)
            else:
                break
        if user_input == User_Input.ROTATE:
            self._rotate()
        return self.cells

    #
    def _rotate(self, rotation):
        raise NotImplementedError('You have to override _rotate in a child class. Don\'t use Block class directly.')


# Class representing the square block. Child class of Block
class Square_Block(Block):
    # I CO Z TEGO, ŻE MISSED?
    def __init__(self, color):
        x = settings.new_block_position.x
        y = settings.new_block_position.y
        self.fields = [
            Cell(x, y, color),
            Cell(x + 1, y, color),
            Cell(x, y + 1, color),
            Cell(x + 1, y + 1, color)
        ]

    def _rotate(self):
        return


# Class representing the L block. Child class of Block
class L_Block(Block):
    def __init__(self, color):
        x = settings.new_block_position.x
        y = settings.new_block_position.y
        self.rotation = 0
        self.fields = [
            Cell(x, y, color),
            Cell(x + 1, y, color),
            Cell(x + 2, y, color),
            Cell(x + 2, y + 1, color)
        ]

    # Calculate fields occupied by the block, depending on its position and rotation properties
    def _rotate(self):
        self.rotation += 90
        if rotation == 0:
            self.fields = [
                Position(x, y),
                Position(x + 1, y),
                Position(x + 2, y),
                Position(x + 2, y + 1)
            ]
        if rotation == 90:
            self.fields = [
                Position(x + 1, y),
                Position(x, y),
                Position(x, y + 1),
                Position(x, y + 2)
            ]
        if rotation == 180:
            self.fields = [
                Position(x, y),
                Position(x, y + 1),
                Position(x + 1, y + 1),
                Position(x + 2, y + 1)
            ]
        if rotation == 270:
            self.fields = [
                Position(x + 1, y),
                Position(x + 1, y + 1),
                Position(x + 1, y + 2),
                Position(x, y + 2)
            ]
        return new_fields
