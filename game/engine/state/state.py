from board import Board
from blocks import create_random_block
from game.engine.key_bindings import User_Input
from key_bindings import User_Input


class Frame:
    # MOZE LEPIEJ SCREEN ZAMIASR BOARD?
    def __init__(self, block, board, sound):
        self.block = block
        self.board = board
        self.sound = sound

class State:
    def __init__(self):
        self.board = Board()
        self.active_block = create_random_block()

    def get_next_frame(self, input):
        new_cells = self.active_block.calculate_new_cells(input)
        is_illegal = self.board.check_if_occupied(new_cells)
        if not is_illegal:
            self.active_block.set_cells(new_cells)
        if input == User_Input.MOVE_DOWN & is_illegal:
            self.board.write_to_board(self.active_block.cells, self.active_block.color)
            self.active_block = create_random_block()
        # MOZE POWINNXM PRZEKAZYWAC NOWE TABLICE ZAMIAST REFERENCJE?
        return Frame(self.active_block, self.board, '')
            