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
# data_dir = os.path.join(main_dir, 'data')

# Initialize global variables
random.seed()
no_of_rows = 12
no_of_columns = 16
# CZY POWINNAM TO ZROBIĆ JAKO KLASĘ?# CZEMU TO NIE DZIALA???
# game_state = [[False]*no_of_rows]*no_of_columns


# Class for keeping the default settings for game objects
class Default_Settings:
    def __init__(self):
        self.block_colors = ['purple', 'yellow', 'green', 'red']
        self.color_to_filename = {
            'purple': 'purple-block.bmp',
            'yellow': 'green-block.bmp',
            'green': 'yellow-block.bmp',
            'red': 'red-block.bmp'
        }
        self.block_rotation = 0
        self.block_position = Position(0, 6)
        self.points_for_rows = {
            0: 0,
            1: 40,
            2: 100,
            3: 300,
            4: 1200
        }


# Class for keeping track of and manipulating current game state and score
class Game_State:
    def __init__(self):
        self.score = 0
        self.state = []
        for i in range(0, no_of_rows):
            row = []
            for j in range(0, no_of_columns):
                # CZY TO POWINNO BYĆ KLASĄ?
                row.append(False)
            self.state.append(row)

    def clear_all_rows(self):
        self.__init__()

    def clear_row(self, index):
        for i in range(index, -1, -1):
            if i > 0:
                game_state.state[i] = game_state.state[i - 1]
            else:
                game_state.state[i] = [False] * no_of_columns


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
        if index == no_of_rows - 1:
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
    print(game_state.state)
    # ## Clear all currently existing sprites and populate sprite groups using loaded game info. This has to be done
    # ## before any methods updating the screen or game state are called to make sure any checks running when new blocks
    # ## are added don't conflict with the current game state
    moving_blocks.empty()
    stationary_blocks.empty()
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
    score = game_info['score_info']
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
        # ## Add necessary info about moving blocks to the object (adding moving_blocks Group causes
        # ## serialization issues; it would also mean serializing and saving redundant data)
        self.moving_blocks_info = []
        for sprite in moving_blocks.sprites():
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
        for sprite in stationary_blocks.sprites():
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
        pg.sprite.Sprite.__init__(self)
        self.position = position
        self.color = color
        game_window = pg.Surface(screen.get_size())
        self.cell_width = game_window.get_width() / no_of_columns
        self.cell_height = game_window.get_height() / no_of_rows
        sprite_filename = default_settings.color_to_filename[color]
        self.image = pg.image.load(os.path.join(assets_dir, sprite_filename)).convert()
        self.image = pg.transform.scale(self.image, (self.cell_width, self.cell_height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.position.y * self.cell_width, self.position.x * self.cell_height)
        self.add(stationary_blocks)


# Abstract class laying groundwork for each type of block in the game
class Block(pg.sprite.Sprite):
    # Initialize key properties used by this class and by child classes
    def __init__(self, position, rotation, color):
        pg.sprite.Sprite.__init__(self)
        self.add(moving_blocks)
        self.color = color
        self.position = position
        self.fields = []
        self.rotation = rotation
        game_window = pg.Surface(screen.get_size())
        self.cell_width = game_window.get_width() / no_of_columns
        self.cell_height = game_window.get_height() / no_of_rows

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
            cell_image = pg.image.load(os.path.join(assets_dir, cell_sprite_filename)).convert()
            cell_image = pg.transform.scale(cell_image, (self.cell_width, self.cell_height))
            dest = (
                (field.y - self.position.y) * self.cell_width,
                (field.x - self.position.x) * self.cell_height
            )
            self.image.blit(cell_image, dest)

    # Stop this block, move it to the stationary_blocks group as individual cells,
    # clear rows if necessary and initialize a new block
    def _stop(self):
        self.remove(moving_blocks)
        for cell_position in self.fields:
            Cell_Sprite(cell_position, self.color)
        # ewentualnie: dodwanie punktów w osobnym miejscu, np. bezpośrednio w pętli gry lub osobna klasa z metodami obśługującymi punktację
        check_and_clear()
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
                if field.x > no_of_rows - 1:
                    collision_vertical = True
                    break
                if field.y > no_of_columns - 1 or field.y < 0:
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
    # ## If type was specified in kwargs, use it. If not, choose a random block type
    if specified_type is not None:
        if specified_type == 'Square_Block':
            block = Square_Block(position, rotation, color)
        elif specified_type == 'L_Block':
            block = L_Block(position, rotation, color)
        elif specified_type == 'Line_Block':
            block = Line_Block(position, rotation, color)
        elif specified_type == 'Diagonal_Block':
            block = Diagonal_Block(position, rotation, color)
        elif specified_type == 'Spaceship_Block':
            block = Spaceship_Block(position, rotation, color)
        elif specified_type == 'Diagonal_Mirror_Block':
            block = Diagonal_Mirror_Block(position, rotation, color)
        elif specified_type == 'L_Mirror_Block':
            block = L_Mirror_Block(position, rotation, color)
    else:
        rand_int = random.randrange(0, 6)
        if rand_int == 0:
            block = Square_Block(position, rotation, color)
        elif rand_int == 1:
            block = L_Block(position, rotation, color)
        elif rand_int == 2:
            block = Line_Block(position, rotation, color)
        elif rand_int == 3:
            block = Diagonal_Block(position, rotation, color)
        elif rand_int == 4:
            block = Spaceship_Block(position, rotation, color)
        elif rand_int == 5:
            block = Diagonal_Mirror_Block(position, rotation, color)
        elif rand_int == 6:
            block = L_Mirror_Block(position, color)
    # ## Check if block's initial fields are available. If not, quit the game
    for field in block.fields:
        if game_state.state[field.x][field.y]:
            pg.display.quit()
            # sprawdzić czy return potrzebny
            return


# Check if any row is filled. If it is, update the score, game state and sprites
def check_and_clear():
    # ## Get cell height and initialize variable keeping track of cleared rows
    game_window = pg.Surface(screen.get_size())
    cell_height = game_window.get_height() / no_of_rows
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
            for sprite in stationary_blocks.sprites():
                if sprite.position.x - index == 0.0:
                    sprite.remove(stationary_blocks)
                if sprite.position.x < index:
                    pg.Rect.move_ip(sprite.rect, 0, cell_height)
    # ## Update the score and print it to the console
    # ma zwracać liczbę punktów i w miejscu wywołania dorzucać do score
    game_state.score += default_settings.points_for_rows[cleared_rows]
    if cleared_rows > 0:
        print(cleared_rows)
        print(f'score: {game_state.score}')


# Initialize objects used by other functions and methods
game_state = Game_State()
default_settings = Default_Settings()
# Initialize variables controlling the game display and clock - frames and ticks
running = True
pg.init()
frame_clock = pg.time.Clock()
frame_counter = 0
screen = pg.display.set_mode((640, 480))
background = pg.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))
screen.blit(background, (0, 0))
pg.display.flip()
# Initialize sprite groups
moving_blocks = pg.sprite.Group()
stationary_blocks = pg.sprite.Group()
# Create the first block
new_block()
# Game loop
while running:
    frame_clock.tick(30)
    frame_counter += 1
    # ## Listen for key inputs and kick off processes creating the expected output
    for event in pg.event.get():
        # ## Key inputs quitting the game
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
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
            moving_blocks.update(direction, rotation)
        # ## Key input for pausing the game
        elif event.type == pg.KEYDOWN and event.key == pg.K_p:
            paused = True
            while paused:
                # ## When paused, tick the frame_clock to be able to react when user clicks the pause button again,
                # ## but don't increase the frame_counter. It should be increased only when the game is actually running
                frame_clock.tick(30)
                for event in pg.event.get():
                    # ## Key input for unpausing
                    if event.type == pg.KEYDOWN and event.key == pg.K_p:
                        paused = False
                    # ## Key inputs quitting the game
                    elif event.type == pg.QUIT:
                        running = False
                        paused = False
                    elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        running = False
                        paused = False
                    # ## Key inputs saving and loading the game
                    elif event.type == pg.KEYDOWN and event.key == pg.K_s:
                        save_game()
                    elif event.type == pg.KEYDOWN and event.key == pg.K_l:
                        load_game()
                        paused = False
    # ## Every 15 ticks move currently moving block down
    if frame_counter >= 15:
        frame_counter = 0
        moving_blocks.update('d', 0)
    # ## Update the display
    screen.blit(background, (0, 0))
    moving_blocks.draw(screen)
    stationary_blocks.draw(screen)
    pg.display.flip()

