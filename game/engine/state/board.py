from settings import settings

class Board:
    def __init__(self):
        self.board = []
        for row in range(0, settings.no_of_rows):
            row = []
            for column in range(0, settings.no_of_columns):
                row.append(False)
            self.board.append(row)  

    def check_if_legal(self, positions):
        for position in positions:
            if (self.board[position.x][position.y] != False and position.x in range (self.no_of_rows) and position.y in range(self.no_of_columns) ):
                return True
        return False

    def write_to_board(self, cells):
        # CZY DOBRZE BY BYLO DODAC HANDLOWANIE PRZEKAZANIA NIE ARRAY?
        for cell in cells:
            self.board[cell.position.x][cell.position.y] = cell.color
