class Screen:
    def __init__(self, board, moving_block) -> None:
        self.board = board
        self.moving_block = moving_block

class Frame:
    # MOZE LEPIEJ SCREEN ZAMIAST BOARD?
    def __init__(self, screen: Screen, sound: str) -> None:
        self.screen = screen
        self.sound = sound

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Cell:
    def __init__(self, x, y, color):
        self.position = Position(x,y)
        self.color = color

class Dimensions:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y