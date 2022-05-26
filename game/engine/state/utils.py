from blocks import Square_Block, L_Block, L_Mirror_Block, Line_Block, Diagonal_Block, Diagonal_Mirror_Block, Spaceship_Block
from game.engine.state.blocks import Block
from settings import settings
from random import randint

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Cell:
    def __init__(self, x, y, color):
        self.position = Position(x,y)
        self.color = color

def create_random_block():
    # PRZENIESC LISTE DOSTEPNYCH TYPOW KLOCKOW DO SETTINGS
    block_types = [Square_Block, L_Block, L_Mirror_Block, Line_Block, Diagonal_Block, Diagonal_Mirror_Block, Spaceship_Block]
    color = settings.colors[randint(0, settings.colors.__len__())]
    block_type = block_types[randint(0, block_types.__len__())]
    return block_type(color)