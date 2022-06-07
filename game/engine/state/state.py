from copy import deepcopy
from state.board import Board
from state.blocks import create_random_block
from key_bindings import User_Input
from utils import Screen


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
        # CO CHCE PRZEKAZYWAC?
        screen = Screen(deepcopy(self.board.board), deepcopy(self.active_block))
        return Frame(screen, '')
            