from engine import Position

class Settings:
    def __init__(self):
        # ## Scoring system
        self.points_for_rows = {
            0: 0,
            1: 40,
            2: 100,
            3: 300,
            4: 1200
        }
        # ## Dimenstions of the game's grid
        self.no_of_rows = 18
        self.no_of_columns = 12
        self.new_block_position = Position(6,0)

settings = Settings()