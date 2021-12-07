# Czy lepiej zrobić tak, że stan gry będzie źródłem wiedzy na temat tego, co na ekranie?
# ambient computing
# pyUnit - do testowania, może jest jakiś dedykowany pygamowi, nawet jeśli nie ma CD to CI w testach ma sens
# baza danych KURSORY
# DEKORATORY w pythonie
# GENERATORY w pythonie
# KONTEKSTY i WITH w pythonie
# SERIALIZACJA DANYCH by zapisaci wczytać (pickle.dump, json.dump)
# SQL injection - bindowanie żeby zabezpieczyć
# TempleOS
# Co to CLOSURE

# Integracja pyCharm - git
# Zrobienie tego online - obgadane
# CI / CD
# praca na repo - branche, updaty itede

import pygame as pg
import os
import random
import json
import datetime

# if not pg.font:
#     print('Warning: fonts disabled')
# if not pg.mixer:
#     print('Warning: sound disabled')
#
main_dir = os.path.split(os.path.abspath(__file__))[0]
assets_dir = os.path.join(main_dir, 'assets')
sprites_dir = os.path.join(assets_dir, 'sprites')
sounds_dir = os.path.join(assets_dir, 'sounds')
# data_dir = os.path.join(main_dir, 'data')

# Initialize random module
random.seed()
# CZEMU TO NIE DZIALA???
# game_state = [[False]*no_of_rows]*no_of_columns


# Class for keeping the default settings for game objects
class Default_Settings:
    def __init__(self):
        # ## Available block names (types) and constructor functions for each name (type)
        self.block_names = ['Square_Block', 'L_Block', 'Line_Block', 'Diagonal_Block', 'Spaceship_Block',
                            'Diagonal_Mirror_Block', 'L_Mirror_Block']
        self.block_name_to_constructor = {
            'Square_Block': lambda position, rotation, color: Square_Block(position, rotation, color),
            'L_Block': lambda position, rotation, color: L_Block(position, rotation, color),
            'Line_Block': lambda position, rotation, color: Line_Block(position, rotation, color),
            'Diagonal_Block': lambda position, rotation, color: Diagonal_Block(position, rotation, color),
            'Spaceship_Block': lambda position, rotation, color: Spaceship_Block(position, rotation, color),
            'Diagonal_Mirror_Block': lambda position, rotation, color: Diagonal_Mirror_Block(position, rotation, color),
            'L_Mirror_Block': lambda position, rotation, color: L_Mirror_Block(position, rotation, color)
        }
        # ## Available block colors and corresponding filenames with cell sprites
        self.block_colors = ['purple', 'yellow', 'green', 'red']
        self.color_to_filename = {
            'purple': 'purple-block.bmp',
            'yellow': 'green-block.bmp',
            'green': 'yellow-block.bmp',
            'red': 'red-block.bmp'
        }
        # ## Default rotation, position of a new block
        self.block_rotation = 0
        self.block_position = Position(0, 5)
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
        # ## Number of next blocks to show
        self.no_of_next_blocks = 3


# Class for keeping track of and manipulating current game state
class Game_State:
    def __init__(self):
        self.score = 0
        # ## When the game_state object is created, fill the game state with Falses
        self.state = []
        for i in range(0, default_settings.no_of_rows):
            row = []
            for j in range(0, default_settings.no_of_columns):
                row.append(False)
            self.state.append(row)
        # ## When the game_state object is created, fill the array of next blocks with random block types
        self.next_blocks = []
        for i in range(0, default_settings.no_of_next_blocks):
            block_types = default_settings.block_names
            block_type = block_types[random.randrange(0, block_types.__len__())]
            self.next_blocks.append(block_type)
        print(self.next_blocks)

    def clear_all_rows(self):
        self.__init__()

    def clear_row(self, index):
        for i in range(index, -1, -1):
            if i > 0:
                game_state.state[i] = game_state.state[i - 1]
            else:
                game_state.state[i] = [False] * default_settings.no_of_columns


# jakich informacji potrzebuję, by odtworzyć stan gry
# tak naprawdę tylko stationary_blocks, moving_blocks i game_state w formie false / true
# no dobrze, a jakich danych z _blocks potrzebuję konkretnie?
# Surface.rect i Surface.image każdego sprite
# to chyba wszystko!


# TYLKO DO DEBUGOWANIA
def print_game_state_pretty():
    for (index, row) in enumerate(game_state.state):
        row_s = ""
        separator = "_____________________________________________________________"
        for column in row:
            if column:
                row_s += 'X\t'
            else:
                row_s += '.\t'
        print(row_s)
        if index == default_settings.no_of_rows - 1:
            print(separator)


# Pauses the game
def pause_game():
    return


# Saves current game state with a timestamp to the savegame file
def save_game():
    game_info = Game_Info()
    game_info_serialized = game_info.toJSON()
    with open('./data/savegames.json', 'w') as file:
        file.write(game_info_serialized)


# Loads last game from the savegame file, update game state, score and display
def load_game():
    # ## load data from savefile and deserialize it
    with open('./data/savegames.json', 'r') as file:
        game_info_serialized = file.read()
        game_info = json.loads(game_info_serialized)
    # ## Clear current game state
    game_state.clear_all_rows()
    # ## Clear all currently existing sprites and populate sprite groups using loaded game info. This has to be done
    # ## before any methods updating the screen or game state are called to make sure any checks running when new blocks
    # ## are added don't conflict with the current game state
    game_display.clear_all_rows()
    # ## Get position and color of each stationary sprite from loaded data and create a new cell sprite using it
    stationary_blocks_info = game_info['stationary_blocks_info']
    for block_info in stationary_blocks_info:
        block_position = Position(block_info['position']['x'], block_info['position']['y'])
        block_color = block_info['color']
        Cell_Sprite(block_position, block_color)
    # ## Get type of block, position, rotation and color of the moving sprite and create a new block using this data
    moving_block_info = game_info['moving_blocks_info'][0]
    moving_block_type = moving_block_info['class_name']
    moving_block_position = Position(moving_block_info['position']['x'], moving_block_info['position']['y'])
    moving_block_rotation = moving_block_info['rotation']
    moving_block_color = moving_block_info['color']
    new_block(type=moving_block_type, position=moving_block_position, rotation=moving_block_rotation, color=moving_block_color)
    # ## Substitute current score with the loaded score
    game_state.score = game_info['score_info']
    # ## Substitute current next_blocks list with the loaded list
    game_state.next_blocks = game_info['next_blocks_info']
    # ## Substitute current game state with the loaded game state. This has to be done after any methods
    # ## updating the screen or game state are called to make sure any checks running when new blocks
    # ## are added don't conflict with the new game state
    game_state.state = game_info['game_state_info']


# Helper class used to extract key information about the game state for saving or sending over the internet
class Game_Info:
    def __init__(self):
        # ## Add current game state to the object
        self.game_state_info = game_state.state
        # ## Add current points to the object
        self.score_info = game_state.score
        # ## Add current next_blocks list to the object
        self.next_blocks_info = game_state.next_blocks
        # ## Add necessary info about moving blocks to the object (adding moving_blocks Group causes
        # ## serialization issues; it would also mean serializing and saving redundant data)
        self.moving_blocks_info = []
        for sprite in game_display.moving_blocks.sprites():
            sprite_info = {
                'class_name': sprite.__class__.__name__,
                'position': sprite.position,
                'color': sprite.color,
                'rotation': sprite.rotation
            }
            self.moving_blocks_info.append(sprite_info)
        # ## Add necessary info about moving blocks to the object (adding stationary Group causes
        # ## serialization issues; it would also mean serializing and saving redundant data)
        self.stationary_blocks_info = []
        for sprite in game_display.stationary_blocks.sprites():
            sprite_info = {
                'position': sprite.position,
                'color': sprite.color
            }
            self.stationary_blocks_info.append(sprite_info)

    def toJSON(self):
        # CZY TAK ROBIĆ TIMESTAMP CZY JAKOŚ INACZEJ?
        self.timestamp = datetime.datetime.now().isoformat()
        return json.dumps(self, default=lambda o: o.__dict__)


# Helper class for keeping track of cells' coordinates
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Helper class for creating sprites representing single cells
class Cell_Sprite(pg.sprite.Sprite):
    def __init__(self, position, color):
        # ## Initialize the sprite
        pg.sprite.Sprite.__init__(self)
        # ## Set position and color
        self.position = position
        self.color = color
        # ## Load sprite from the filesystem to self.image and use it to define self.rect
        sprite_filename = default_settings.color_to_filename[color]
        cell_height = game_display.game_cell_height
        cell_width = game_display.game_cell_width
        self.image = pg.image.load(os.path.join(sprites_dir, sprite_filename)).convert()
        self.image = pg.transform.scale(self.image, (cell_width, cell_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.position.y * cell_width, self.position.x * cell_height)
        # ## Add the sprite to the stationary_blocks group
        self.add(game_display.stationary_blocks)


# Abstract class laying groundwork for each type of block in the game
class Block(pg.sprite.Sprite):
    # Initialize key properties used by this class and by child classes
    def __init__(self, position, rotation, color):
        pg.sprite.Sprite.__init__(self)
        self.add(game_display.moving_blocks)
        self.color = color
        self.position = position
        self.fields = []
        self.rotation = rotation
        game_window = pg.Surface(game_display.game_area.get_size())
        # CZY TO POWINNO BYĆ ZDEFINIOWANE TUTAJ, CZY KAŻDORAZOWO ODWOŁANIE DO GAME_DISPLAY?
        self.cell_width = game_display.game_cell_width
        self.cell_height = game_display.game_cell_height

    # Create an image of the block sprite
    def draw(self):
        # ## Create a 3x3 canvas on which the block will be drawn, extract its rect and position it properly
        self.image = pg.Surface((3 * self.cell_width, 3 * self.cell_height))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.position.y * self.cell_width, self.position.x * self.cell_height)
        # ## Draw each individual cell onto the canvas
        for field in self.fields:
            cell_sprite_filename = default_settings.color_to_filename[self.color]
            cell_image = pg.image.load(os.path.join(sprites_dir, cell_sprite_filename)).convert()
            cell_image = pg.transform.scale(cell_image, (self.cell_width, self.cell_height))
            dest = (
                (field.y - self.position.y) * self.cell_width,
                (field.x - self.position.x) * self.cell_height
            )
            self.image.blit(cell_image, dest)

    # Stop this block, move it to the stationary_blocks group as individual cells,
    # clear rows if necessary and initialize a new block
    def _stop(self):
        self.remove(game_display.moving_blocks)
        for cell_position in self.fields:
            Cell_Sprite(cell_position, self.color)
        # ewentualnie: dodwanie punktów w osobnym miejscu, np. bezpośrednio w pętli gry lub osobna klasa z metodami obśługującymi punktację
        check_and_clear()
        print(game_state.next_blocks)
        new_block()

    # Move or rotate the block if possible, detect collisions and act accordingly
    def _move(self, direction, rotation):
        # ## Print an error if block has no fields
        if len(self.fields) == 0:
            print('Error! This block has no fields (self.fields has length 0)!')
            return
        else:
            # ## Calculate block's rotation, position and occupied fields after the move
            new_rotation = (self.rotation + rotation) % 360
            new_position = self.position
            if direction == 'l':
                new_position = Position(self.position.x, self.position.y - 1)
            if direction == 'r':
                new_position = Position(self.position.x, self.position.y + 1)
            if direction == 'd':
                new_position = Position(self.position.x + 1, self.position.y)
            new_fields = self.calculate_fields(new_position.x, new_position.y, new_rotation)
            # ## Remove fields representing block's cells from the game state
            # ## (it's necessary for proper collision detection)
            for field in self.fields:
                game_state.state[field.x][field.y] = False
            # ## Detect collisions with borders and other blocks
            collision_horizontal = False
            collision_vertical = False
            for field in new_fields:
                # ## Detecting collisions with borders must come first, as game_state doesn't exist outside of them
                if field.x > default_settings.no_of_rows - 1:
                    collision_vertical = True
                    break
                if field.y > default_settings.no_of_columns - 1 or field.y < 0:
                    collision_horizontal = True
                    break
                # ## Detect collisions with other blocks
                if game_state.state[field.x][field.y]:
                    if direction in ('l', 'r') or rotation != 0:
                        collision_horizontal = True
                    if direction == 'd':
                        collision_vertical = True
            # ## If no collision was detected, update block's properties with new values
            if not collision_horizontal and not collision_vertical:
                self.position = new_position
                self.fields = new_fields
                self.rotation = new_rotation
            # ## Whether block's properties were updated after collision detection or not, insert their representation
            # ## back into the game state
            for field in self.fields:
                game_state.state[field.x][field.y] = True
            # ## If vertical collision was detected, stop the block. This has to be checked after updating game state
            # ## to make sure that the _stop function uses current state
            if collision_vertical:
                self._stop()

    # This method will be called by the sprite group and contains methods that should be executed each tick
    def update(self, direction, rotation):
        self._move(direction, rotation)
        self.draw()

    # Abstract method indicating that every child class should implement it separately
    # raise exception instead of printing
    def calculate_fields(self, x, y, rotation):
        print("Error! calculate_fields class must be defined in a child class")
        return


# Class representing the square block. Child class of Block
class Square_Block(Block):
    def __init__(self, position, rotation, color):
        super().__init__(position, rotation, color)
        self.fields = self.calculate_fields(self.position.x, self.position.y, self.rotation)
        self.draw()

    # Calculate fields occupied by the block, depending on its position and rotation properties
    def calculate_fields(self, x, y, rotation):
        new_fields = [
            Position(x, y),
            Position(x + 1, y),
            Position(x, y + 1),
            Position(x + 1, y + 1)
        ]
        return new_fields


# Class representing the L block. Child class of Block
class L_Block(Block):
    def __init__(self, position, rotation, color):
        super().__init__(position, rotation, color)
        self.fields = self.calculate_fields(self.position.x, self.position.y, self.rotation)
        self.draw()

    # Calculate fields occupied by the block, depending on its position and rotation properties
    def calculate_fields(self, x, y, rotation):
        if rotation == 0:
            new_fields = [
                Position(x, y),
                Position(x + 1, y),
                Position(x + 2, y),
                Position(x + 2, y + 1)
            ]
        if rotation == 90:
            new_fields = [
                Position(x + 1, y),
                Position(x, y),
                Position(x, y + 1),
                Position(x, y + 2)
            ]
        if rotation == 180:
            new_fields = [
                Position(x, y),
                Position(x, y + 1),
                Position(x + 1, y + 1),
                Position(x + 2, y + 1)
            ]
        if rotation == 270:
            new_fields = [
                Position(x + 1, y),
                Position(x + 1, y + 1),
                Position(x + 1, y + 2),
                Position(x, y + 2)
            ]
        return new_fields


# Class representing the mirrored L block. Child class of Block
class L_Mirror_Block(Block):
    def __init__(self, position, rotation, color):
        super().__init__(position, rotation, color)
        self.fields = self.calculate_fields(self.position.x, self.position.y, self.rotation)
        self.draw()

    # Calculate fields occupied by the block, depending on its position and rotation properties
    def calculate_fields(self, x, y, rotation):
        if rotation == 0:
            new_fields = [
                Position(x, y + 1),
                Position(x + 1, y + 1),
                Position(x + 2, y + 1),
                Position(x + 2, y)
            ]
        if rotation == 90:
            new_fields = [
                Position(x, y),
                Position(x + 1, y),
                Position(x + 1, y + 1),
                Position(x + 1, y + 2)
            ]
        if rotation == 180:
            new_fields = [
                Position(x, y + 1),
                Position(x, y),
                Position(x + 1, y),
                Position(x + 2, y)
            ]
        if rotation == 270:
            new_fields = [
                Position(x, y),
                Position(x, y + 1),
                Position(x, y + 2),
                Position(x + 1, y + 2)
            ]
        return new_fields


# Class representing the vertical line block. Child class of Block
class Line_Block(Block):
    def __init__(self, position, rotation, color):
        super().__init__(position, rotation, color)
        self.fields = self.calculate_fields(self.position.x, self.position.y, self.rotation)
        self.draw()

    # Calculate fields occupied by the block, depending on its position and rotation properties
    def calculate_fields(self, x, y, rotation):
        if rotation in (0, 180):
            new_fields = [
                Position(x, y),
                Position(x + 1, y),
                Position(x + 2, y),
            ]
        elif rotation in (90, 270):
            new_fields = [
                Position(x + 1, y),
                Position(x + 1, y + 1),
                Position(x + 1, y + 2),
            ]
        return new_fields


# Class representing the diagonal block. Child class of Block
class Diagonal_Block(Block):
    def __init__(self, position, rotation, color):
        super().__init__(position, rotation, color)
        self.fields = self.calculate_fields(self.position.x, self.position.y, self.rotation)
        self.draw()

    # Calculate fields occupied by the block, depending on its position and rotation properties
    def calculate_fields(self, x, y, rotation):
        if rotation in (0, 180):
            new_fields = [
                Position(x, y),
                Position(x + 1, y),
                Position(x + 1, y + 1),
                Position(x + 2, y + 1)
            ]
        elif rotation in (90, 270):
            new_fields = [
                Position(x + 1, y),
                Position(x + 1, y + 1),
                Position(x, y + 1),
                Position(x, y + 2)
            ]
        return new_fields


# Class representing the mirrored diagonal block. Child class of Block
class Diagonal_Mirror_Block(Block):
    def __init__(self, position, rotation, color):
        super().__init__(position, rotation, color)
        self.fields = self.calculate_fields(self.position.x, self.position.y, self.rotation)
        self.draw()

    # Calculate fields occupied by the block, depending on its position and rotation properties
    def calculate_fields(self, x, y, rotation):
        if rotation in (0, 180):
            new_fields = [
                Position(x, y + 1),
                Position(x + 1, y + 1),
                Position(x + 1, y),
                Position(x + 2, y)
            ]
        elif rotation in (90, 270):
            new_fields = [
                Position(x, y),
                Position(x, y + 1),
                Position(x + 1, y + 1),
                Position(x + 1, y + 2)
            ]
        return new_fields


# Class representing the spaceship block. Child class of Block
class Spaceship_Block(Block):
    def __init__(self, position, rotation, color):
        super().__init__(position, rotation, color)
        self.fields = self.calculate_fields(self.position.x, self.position.y, self.rotation)
        self.draw()

    # Calculate fields occupied by the block, depending on its position and rotation properties
    def calculate_fields(self, x, y, rotation):
        if rotation == 0:
            new_fields = [
                Position(x, y),
                Position(x + 1, y),
                Position(x + 1, y + 1),
                Position(x + 2, y)
            ]
        if rotation == 90:
            new_fields = [
                Position(x, y),
                Position(x, y + 1),
                Position(x + 1, y + 1),
                Position(x, y + 2)
            ]
        if rotation == 180:
            new_fields = [
                Position(x, y + 1),
                Position(x + 1, y + 1),
                Position(x + 1, y),
                Position(x + 2, y + 1)
            ]
        if rotation == 270:
            new_fields = [
                Position(x + 1, y),
                Position(x + 1, y + 1),
                Position(x, y + 1),
                Position(x + 1, y + 2)
            ]
        return new_fields


# Create a new block, if possible. If not, exit the game
def new_block(**kwargs):
    # ## If type, color or position was specified, retrieve it from dict with keyword arguments
    specified_type = kwargs.get('type')
    specified_color = kwargs.get('color')
    specified_position = kwargs.get('position')
    specified_rotation = kwargs.get('rotation')
    # ## If position was specified in kwargs, use it. If not, use default position
    if specified_position is not None:
        position = specified_position
    else:
        position = default_settings.block_position
    # ## If rotation was specified in kwargs, use it. If not, use default value
    if specified_rotation is not None:
        rotation = specified_rotation
    else:
        rotation = default_settings.block_rotation
    # ## If color was specified in kwargs, use it. If not, choose a random color
    if specified_color is not None:
        color = specified_color
    else:
        # ## Draw a random color
        colors = default_settings.block_colors
        color = colors[random.randrange(0, colors.__len__())]
    # ## If type was specified in kwargs, use it. If not, choose a the next block from the game_state.next_blocks list
    if specified_type is not None:
        block_constructor = default_settings.block_name_to_constructor[specified_type]
        block = block_constructor(position, rotation, color)
    else:
        # ## Take the first block from the game_state.next_blocks list, then delete it from the list and add a new
        # ## block at the end
        next_blocks = game_state.next_blocks
        types = default_settings.block_names
        type = next_blocks[0]
        type_to_append = types[random.randrange(0, types.__len__())]
        next_blocks.append(type_to_append)
        game_state.next_blocks = next_blocks[1:]
        # ## Get the block constructor function and run it with appropriate arguments
        block_constructor = default_settings.block_name_to_constructor[type]
        block = block_constructor(position, rotation, color)
    # ## Check if block's initial fields are available. If not, end the game
    for field in block.fields:
        if game_state.state[field.x][field.y]:
            # JAK ZROBIĆ ŻEBY NIE SIĘGAĆ DO TEGO OBIEKTU? ZWRACANIE RZECZY PRZEZ FUNKCJE?
            game_loops.game_finished = True


# Check if any row is filled. If it is, update the score, game state and sprites
def check_and_clear():
    # ## Initialize variable keeping track of cleared rows
    cleared_rows = 0
    # ## For each row, calculate if it is full. If it is, remove the row from game state and from the screen, then
    # ## update all cells above the deleted row so they fall into emptied space both on screen and in game state
    for (index, row) in enumerate(game_state.state):
        row_full = True
        for column in row:
            if not column:
                row_full = False
                break
        if row_full:
            cleared_rows += 1
            game_state.clear_row(index)
            game_display.clear_row(index)

    # ## Update the score and print it to the console
    # ma zwracać liczbę punktów i w miejscu wywołania dorzucać do score
    game_state.score += default_settings.points_for_rows[cleared_rows]
    if cleared_rows > 0:
        print(cleared_rows)
        print(f'score: {game_state.score}')
        # ## Play the row_cleared sound
        game_sounds.play_row_cleared()


# Class with methods and properties representing current display
class Game_Display:
    def __init__(self):
        # ## Create main display
        self.display = pg.display.set_mode((600, 600))
        # ## Create game area and its background
        # ## Background ratio - 2:3
        self.game_area = pg.Surface((400, 600))
        self.game_area = self.game_area.convert()
        self.game_area.fill((255, 255, 255))
        self.game_area_background = pg.Surface(self.game_area.get_size())
        self.game_area_background = self.game_area_background.convert()
        self.game_area_background.fill((255, 255, 255))
        # ## Calculate cell dimensions
        self.game_cell_height = self.game_area.get_height() / default_settings.no_of_rows
        self.game_cell_width = self.game_area.get_width() / default_settings.no_of_columns
        # ## Create UI area and its background
        self.ui_area = pg.Surface((200, 600))
        self.ui_area = self.ui_area.convert()
        self.ui_area.fill((0, 0, 0))
        self.ui_area_background = pg.Surface(self.ui_area.get_size())
        self.ui_area_background = self.ui_area_background.convert()
        self.ui_area_background.fill((0, 0, 0))
        # ## Create main menu and its background
        self.main_menu = pg.Surface((600, 600))
        self.main_menu = self.main_menu.convert()
        self.main_menu.fill((0, 0, 0))
        # ## Create endgame screen and its background
        self.end_game_menu = pg.Surface((600, 600))
        self.end_game_menu = self.main_menu.convert()
        self.end_game_menu.fill((0, 0, 0))
        # ## Initialize sprite groups
        self.stationary_blocks = pg.sprite.Group()
        self.moving_blocks = pg.sprite.Group()

    # Draws the main menu
    def draw_main_menu(self):
        text_antialiased = True
        text_color = (255, 255, 255)
        my_font = pg.font.SysFont('Console', 40)
        my_font_small = pg.font.SysFont('Console', 25)
        main_text = my_font.render('Tetris', text_antialiased, text_color)
        main_text_size = my_font.size('Tetris')
        sub_text_1 = my_font_small.render('Wciśnij \'s\' by rozpocząć nową grę', text_antialiased, text_color)
        sub_text_1_size = my_font_small.size('Wciśnij \'s\' by rozpocząć nową grę')
        sub_text_2 = my_font_small.render('Wciśnij Esc by kontynuować grę', text_antialiased, text_color)
        sub_text_2_size = my_font_small.size('Wciśnij Esc by kontynuować grę')
        self.main_menu.blit(main_text, ((600 - main_text_size[0]) / 2, 200))
        self.main_menu.blit(sub_text_1, ((600 - sub_text_1_size[0]) / 2, 300))
        self.main_menu.blit(sub_text_2, ((600 - sub_text_2_size[0]) / 2, 350))
        self.display.blit(self.main_menu, (0, 0))
        pg.display.flip()

    # Draw the endgame screen
    def draw_end_game_menu(self):
        text_antialiased = True
        text_color = (255, 255, 255)
        my_font = pg.font.SysFont('Console', 40)
        my_font_small = pg.font.SysFont('Console', 25)
        main_text = my_font.render(f'Zdobyłxś {game_state.score} pkt', text_antialiased, text_color)
        main_text_size = my_font.size(f'Zdobyłxś {game_state.score} pkt')
        sub_text = my_font_small.render('Wciśnij Esc by wrócić do menu głównego', text_antialiased, text_color)
        sub_text_size = my_font_small.size('Wciśnij Esc by wrócić do menu głównego')
        self.end_game_menu.blit(main_text, ((600 - main_text_size[0]) / 2, 200))
        self.end_game_menu.blit(sub_text, ((600 - sub_text_size[0]) / 2, 300))
        self.display.blit(self.end_game_menu, (0, 0))
        pg.display.flip()

    # Blits all game areas to the main display and flips it
    def update_game_display(self):
        self.display.blit(self.ui_area, (400, 0))
        self.display.blit(self.game_area, (0, 0))
        pg.display.flip()

    # Draws game sprites to the game area
    def draw_game_sprites(self):
        # ## First, blit the background to draw over
        self.game_area.blit(self.game_area_background, (0, 0))
        # ## Draw the sprites
        self.stationary_blocks.draw(self.game_area)
        self.moving_blocks.draw(self.game_area)

    # Draws UI sprites to the UI area
    def draw_ui_sprites(self):
        # ## First, blit the background to draw over
        self.ui_area.blit(self.ui_area_background, (0, 0))
        # ## Write info in the UI area
        my_font = pg.font.SysFont('Console', 25)
        my_font_small = pg.font.SysFont('Console', 18)
        text_antialiased = True
        text_color = (255, 255, 255)
        # ##
        score_title = my_font.render('Wynik:', text_antialiased, text_color)
        score_title_size = my_font.size('Wynik:')
        # ##
        score_value = my_font.render(f'{game_state.score}', text_antialiased, text_color)
        score_value_size = my_font.size(f'{game_state.score}')
        # ##
        keys_title = my_font.render('Sterowanie:', text_antialiased, text_color)
        key_1 = my_font_small.render('R - obróć klocek', text_antialiased, text_color)
        # key_2 = my_font_small.render('strzałki - ruszaj klockiem', text_antialiased, text_color)
        key_3 = my_font_small.render('S - zapisz grę', text_antialiased, text_color)
        key_4 = my_font_small.render('L - ładuj grę', text_antialiased, text_color)
        key_5 = my_font_small.render('P - zatrzymaj grę', text_antialiased, text_color)
        keys_title_size = my_font.size('Sterowanie:')
        key_1_size = my_font_small.size('R - obróć klocek')
        # key_2_size = my_font_small.size('strzałki - ruszaj klockiem')
        key_3_size = my_font_small.size('S - zapisz grę')
        key_4_size = my_font_small.size('L - ładuj grę')
        key_5_size = my_font_small.size('P - zatrzymaj grę')
        self.ui_area.blit(score_title, ((200 - score_title_size[0])/2, 120))
        self.ui_area.blit(score_value, ((200 - score_value_size[0])/2, 160))
        self.ui_area.blit(keys_title, ((200 - keys_title_size[0]) / 2, 300))
        self.ui_area.blit(key_1, ((200 - key_1_size[0]) / 2, 330))
        # self.ui_area.blit(key_2, (400 + (200 - key_2_size[0]) / 2, 150))
        self.ui_area.blit(key_3, ((200 - key_3_size[0]) / 2, 360))
        self.ui_area.blit(key_4, ((200 - key_4_size[0]) / 2, 390))
        self.ui_area.blit(key_5, ((200 - key_5_size[0]) / 2, 420))

    # Removes sprites from one row, updates position property of the sprites above and moves them down on the display
    def clear_row(self, x_position):
        for sprite in self.stationary_blocks.sprites():
            if sprite.position.x - x_position == 0.0:
                sprite.remove(self.stationary_blocks)
            if sprite.position.x < x_position:
                pg.Rect.move_ip(sprite.rect, 0, self.game_cell_height)
                sprite.position = Position(sprite.position.x + 1, sprite.position.y)

    # Removes all existing sprites from respective sprite groups
    def clear_all_rows(self):
        self.moving_blocks.empty()
        self.stationary_blocks.empty()


# Class with methods and properties controlling game music and sounds
class Game_Sounds:
    # CZY TUTAJ W INIT NALEŻY ZAINICJOWAĆ MODUŁ PYGAME? TO SAMO PYTANIE W GAME_DISPLAY
    def __init__(self):
        self.main_theme = pg.mixer.Sound(os.path.join(sounds_dir, 'main_theme.mp3'))
        self.row_cleared = pg.mixer.Sound(os.path.join(sounds_dir, 'row_cleared.wav'))

    def play_main_theme(self):
        pg.mixer.Sound.play(self.main_theme)

    def play_row_cleared(self):
        pg.mixer.Sound.play(self.row_cleared)


class Game_Loops:
    def __init__(self):
        # TO RACZEJ JEDNAK NIE TUTAJ
        pg.init()
        self.game_running = True
        self.game_finished = False
        self.frame_clock = pg.time.Clock()
        self.frame_counter = 0
        # Key game controls, used by multiple methods
        self.leave_game = pg.QUIT

    def main_menu(self):
        in_menu = True
        while in_menu and self.game_running:
            self.frame_clock.tick(30)
            for event in pg.event.get():
                # ## Key inputs quitting the game
                if event.type == self.leave_game:
                    self.game_running = False
                    in_menu = False
                # ## If Esc is clicked, go back to the game
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    self._game()
                # ## If s is clicked, clear current game and start a new one
                elif event.type == pg.KEYDOWN and event.key == pg.K_s:
                    self.game_finished = False
                    game_state.clear_all_rows()
                    game_state.score = 0
                    game_display.clear_all_rows()
                    game_display.moving_blocks.empty()
                    new_block()
                    self._game()
            game_display.draw_main_menu()

    def _game(self):
        playing = True
        while playing and self.game_running:
            self.frame_clock.tick(30)
            self.frame_counter += 1
            # ## Listen for key inputs and kick off processes creating the expected output
            for event in pg.event.get():
                # ## Key inputs quitting the game
                if event.type == self.leave_game:
                    self.game_running = False
                    playing = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    playing = False
                # ## Key inputs saving and loading the game
                elif event.type == pg.KEYDOWN and event.key == pg.K_s:
                    save_game()
                elif event.type == pg.KEYDOWN and event.key == pg.K_l:
                    load_game()
                # ## Key inputs controlling currently moving block's movement
                elif event.type == pg.KEYDOWN and event.key in (pg.K_RIGHT, pg.K_LEFT, pg.K_DOWN, pg.K_r):
                    direction = ''
                    rotation = 0
                    if event.key == pg.K_RIGHT:
                        direction = 'r'
                    if event.key == pg.K_LEFT:
                        direction = 'l'
                    if event.key == pg.K_DOWN:
                        direction = 'd'
                    if event.key == pg.K_r:
                        rotation = 90
                    game_display.moving_blocks.update(direction, rotation)
            # ## Every 15 ticks move currently moving block down
            if self.frame_counter >= 15:
                self.frame_counter = 0
                game_display.moving_blocks.update('d', 0)
                if self.game_finished:
                    playing = False
                    self._end_game()
            # ## Draw the sprites and update the display
            game_display.draw_game_sprites()
            game_display.draw_ui_sprites()
            game_display.update_game_display()

    def _end_game(self):
        in_end_game = True
        while in_end_game and self.game_running:
            self.frame_clock.tick(30)
            for event in pg.event.get():
                # ## Key inputs quitting the game
                if event.type == self.leave_game:
                    self.game_running = False
                    in_end_game = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    in_end_game = False
                elif event.type == pg.KEYDOWN and event.key == pg.K_s:
                    self._game()
            game_display.draw_end_game_menu()

# Pauses the game until player presses the unpause button
# def pause_game():
#     paused = True
#     while paused:
#         # ## When paused, tick the frame_clock to be able to react when user clicks the pause button again,
#         # ## but don't increase the frame_counter. It should be increased only when the game is actually running
#         frame_clock.tick(30)
#         for event in pg.event.get():
#             # ## Key input for unpausing
#             if event.type == pg.KEYDOWN and event.key == pg.K_p:
#                 paused = False
#             # ## Key inputs quitting the game
#             elif event.type == pg.QUIT:
#                 running = False
#                 paused = False
#             elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
#                 running = False
#                 paused = False
#             # ## Key inputs saving and loading the game
#             elif event.type == pg.KEYDOWN and event.key == pg.K_s:
#                 save_game()
#             elif event.type == pg.KEYDOWN and event.key == pg.K_l:
#                 load_game()
#                 paused = False


# Starts the game
# def play_game():
    # playing = True
    # # ## frame_counter should be declared outside of the function to make sure that pausing the game won't influence it
    # # CZY TO JEST DOBRZE??? (GLOBAL)
    # global frame_counter
    # while playing:
    #     frame_clock.tick(30)
    #     frame_counter += 1
    #     # ## Listen for key inputs and kick off processes creating the expected output
    #     for event in pg.event.get():
    #         # ## Key inputs quitting the game
    #         if event.type == pg.QUIT:
    #             playing = False
    #         elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
    #             playing = False
    #         # ## Key inputs saving and loading the game
    #         elif event.type == pg.KEYDOWN and event.key == pg.K_s:
    #             save_game()
    #         elif event.type == pg.KEYDOWN and event.key == pg.K_l:
    #             load_game()
    #         # ## Key inputs controlling currently moving block's movement
    #         elif event.type == pg.KEYDOWN and event.key in (pg.K_RIGHT, pg.K_LEFT, pg.K_DOWN, pg.K_r):
    #             direction = ''
    #             rotation = 0
    #             if event.key == pg.K_RIGHT:
    #                 direction = 'r'
    #             if event.key == pg.K_LEFT:
    #                 direction = 'l'
    #             if event.key == pg.K_DOWN:
    #                 direction = 'd'
    #             if event.key == pg.K_r:
    #                 rotation = 90
    #             game_display.moving_blocks.update(direction, rotation)
    #         # ## Key input for pausing the game
    #         elif event.type == pg.KEYDOWN and event.key == pg.K_p:
    #             pause_game()
    #     # ## Every 15 ticks move currently moving block down
    #     if frame_counter >= 15:
    #         frame_counter = 0
    #         game_display.moving_blocks.update('d', 0)
    #     # ## Draw the sprites and update the display
    #     game_display.draw_game_sprites()
    #     game_display.draw_ui_sprites()
    #     game_display.update_game_display()


# Displays the main menu
# def main_menu():
#     in_menu = True
#     while in_menu:
#         frame_clock.tick(30)
#         for event in pg.event.get():
#             # ## Key inputs quitting the game
#             if event.type == pg.QUIT:
#                 in_menu = False
#             elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
#                 in_menu = False
#             elif event.type == pg.KEYDOWN and event.key == pg.K_s:
#                 play_game()
#         game_display.draw_main_menu()


# Displays the end game menu
# def end_game_menu():
#     return

# Initialize pyGame module and game clock
pg.init()
frame_clock = pg.time.Clock()
frame_counter = 0
# Initialize objects used by other functions and methods
default_settings = Default_Settings()
game_state = Game_State()
game_display = Game_Display()
game_sounds = Game_Sounds()
game_loops = Game_Loops()
# Create the first block
new_block()
# Play the main theme
game_sounds.play_main_theme()
# Initialize the game
game_loops.main_menu()