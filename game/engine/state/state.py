from copy import deepcopy
from board import Board
from blocks import create_random_block
from game.engine.key_bindings import User_Input
from key_bindings import User_Input


class Frame:
    # MOZE LEPIEJ SCREEN ZAMIAST BOARD?
    def __init__(self, screen, sound):
        self.screen = screen
        self.sound = sound

class State:
    def __init__(self):
        self.board = Board()
        self.active_block = create_random_block()

    def get_next_frame(self, input: str) -> Frame:
        new_cells = self.active_block.calculate_new_cells(input)
        is_illegal = self.board.check_if_occupied(new_cells)
        if not is_illegal:
            self.active_block.set_cells(new_cells)
        if input == User_Input.MOVE_DOWN & is_illegal:
            self.board.write_to_board(self.active_block.cells)
            self.active_block = create_random_block()
        # MOZE POWINNXM PRZEKAZYWAC NOWE TABLICE ZAMIAST REFERENCJE?
        screen = deepcopy(self.board)
        screen.write_to_board(self.active_block.cells)
        return Frame(screen, '')
            