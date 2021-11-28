# Czy lepiej zrobić tak, że stan gry będzie źródłem wiedzy na temat tego, co na ekranie?
# pyUnit - do testowania, może jest jakiś dedykowany pygamowi, nawet jeśli nie ma CD to CI w testach ma sens
# baza danych KURSORY
# DEKORATORY w pythonie
# GENERATORY w pythonie
# KONTEKSTY i WITH w pythonie
# SERIALIZACJA DANYCH by zapisaci wczytać (pickle.dump, json.dump)
# SQL injection - bindowanie żeby zabezpieczyć

# Integracja pyCharm - git
# Zrobienie tego online - obgadane
# CI / CD
# praca na repo - branche, updaty itede

import pygame as pg
# import os
import random
import datetime

# if not pg.font:
#     print('Warning: fonts disabled')
# if not pg.mixer:
#     print('Warning: sound disabled')
#
# main_dir = os.path.split(os.path.abspath(__file__))[0]
# data_dir = os.path.join(main_dir, 'data')

# Initialize global variables
no_of_rows = 12
no_of_columns = 16
score = 0
# CZY POWINNAM TO ZROBIĆ JAKO KLASĘ?
points_for_rows = {
    0: 0,
    1: 40,
    2: 100,
    3: 300,
    4: 1200
}
# CZEMU TO NIE DZIALA???
# game_state = [[False]*no_of_rows]*no_of_columns

# Create game state - a table of rows
game_state = []
for i in range(0, no_of_rows):
    row = []
    for j in range(0, no_of_columns):
        # CZY TO POWINNO BYĆ KLASĄ?
        row.append({
            'occupied': False,
            'color': None
        })
    game_state.append(row)


# TYLKO DO DEBUGOWANIA
def print_game_state_pretty():
    for (index, row) in enumerate(game_state):
        row_s = ""
        separator = "_____________________________________________________________"
        for column in row:
            if column['occupied']:
                color = column['color']
                row_s += f'X, {color}\t'
            else:
                row_s += '.\t'
        print(row_s)
        if index == no_of_rows - 1:
            print(separator)


# Saves current game state with a timestamp to the savegame file
def save_game():
    cur_moving_sprite = moving_blocks.sprites()[0]
    with open('./data/savegames.txt', 'a') as file:
        savegame = f'' \
                   f'{datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}\n' \
                   f'{game_state}\n' \
                   f'{score}\n' \
                   f'{cur_moving_sprite.__class__.__name__}\n' \
                   f'{cur_moving_sprite.position.x},{cur_moving_sprite.position.y}\n\n'
        file.write(savegame)
    print("Game saved!")


# Loads last game from the savegame file, updated game state, display and classes containing blocks
def load_game():
    # pobierz dane z pliku, ustaw stan gry, ekran i punkty
    return


# Helper class for keeping track of cells' coordinates
class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Helper class for creating sprites representing single cells
class Cell_Sprite(pg.sprite.Sprite):
    def __init__(self, color):
        pg.sprite.Sprite.__init__(self)
        game_window = pg.Surface(screen.get_size())
        self.cell_width = game_window.get_width() / no_of_columns
        self.cell_height = game_window.get_height() / no_of_rows
        self.image = pg.Surface((self.cell_width, self.cell_height))
        self.image.fill(color)
        self.rect = self.image.get_rect()


# Abstract class laying groundwork for each type of block in the game
class Block(pg.sprite.Sprite):
    # Initialize key properties used by this class and by child classes
    def __init__(self, color):
        pg.sprite.Sprite.__init__(self)
        self.add(moving_blocks)
        self.color = color
        self.position = Position(0, 7)
        self.fields = []
        self.rotation = 0
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
            field_surface = pg.Surface((self.cell_width, self.cell_height))
            field_surface.fill(self.color)
            dest = (
                (field.y - self.position.y) * self.cell_width,
                (field.x - self.position.x) * self.cell_height
            )
            self.image.blit(field_surface, dest)

    # Stop this block, move it to the stationary_blocks group as individual cells,
    # clear rows if necessary and initialize a new block
    def _stop(self):
        self.remove(moving_blocks)
        for cell_position in self.fields:
            cell_sprite = Cell_Sprite(self.color)
            cell_sprite.rect.topleft = (cell_position.y * self.cell_width, cell_position.x * self.cell_height)
            cell_sprite.add(stationary_blocks)
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
                game_state[field.x][field.y] = {
                    'occupied': False,
                    'color': None
                }
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
                if game_state[field.x][field.y]['occupied']:
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
                game_state[field.x][field.y] = {
                    'occupied': True,
                    'color': self.color
                }
            # ## If vertical collision was detected, stop the block. This has to be checked after updating game state
            # ## to make sure that the _stop function uses current state
            if collision_vertical:
                self._stop()

    # This method will be called by the sprite group and contains methods that should be executed each tick
    def update(self, direction, rotation):
        self._move(direction, rotation)
        self.draw()

    # Abstract method indicating that every child class should implement it separately
    def calculate_fields(self, x, y):
        print("Error! calculate_fields class must be defined in a child class")
        return


# Class representing the square block. Child class of Block
class Square_Block(Block):
    def __init__(self, color):
        super().__init__(color)
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
    def __init__(self, color):
        super().__init__(color)
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


# Class representing the vertical line block. Child class of Block
class Line_Block(Block):
    def __init__(self, color):
        super().__init__(color)
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
    def __init__(self, color):
        super().__init__(color)
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


# Create a new block, if possible. If not, exit the game
def new_block():
    # ## Draw a random color and type of block
    random.seed()
    colors = [
        (229, 57, 53),
        (30, 136, 229),
        (142, 36, 170),
        (0, 137, 123),
    ]
    color = colors[random.randrange(0, colors.__len__())]
    random.seed()
    rand_int = random.randrange(0, 4)
    if rand_int == 0:
        block = Square_Block(color)
    elif rand_int == 1:
        block = L_Block(color)
    elif rand_int == 2:
        block = Line_Block(color)
    elif rand_int == 3:
        block = Diagonal_Block(color)
    # ## Check if block's initial fields are available. If not, quit the game
    no_room_for_new_block = False
    for field in block.fields:
        if game_state[field.x][field.y]['occupied']:
            no_room_for_new_block = True
    if no_room_for_new_block:
        pg.display.quit()


# Check if any row is filled. If it is, update the score, game state and sprites
def check_and_clear():
    # ## Get cell height and initialize variable keeping track of cleared rows
    game_window = pg.Surface(screen.get_size())
    cell_height = game_window.get_height() / no_of_rows
    cleared_rows = 0
    # ## For each row, calculate if it is full. If it is, remove the row from game state and from the screen, then
    # ## update all cells above the deleted row so they fall into emptied space both on screen and in game state
    for (index, row) in enumerate(game_state):
        row_full = True
        for column in row:
            if not column['occupied']:
                row_full = False
                break
        if row_full:
            cleared_rows += 1
            for i in range(index, -1, -1):
                if i > 0:
                    game_state[i] = game_state[i - 1]
                else:
                    game_state[i] = [{
                        'occupied': False,
                        'color': None
                    }]*no_of_columns
            for sprite in stationary_blocks.sprites():
                if sprite.rect.y - index * cell_height == 0.0:
                    sprite.remove(stationary_blocks)
                if sprite.rect.y < index * cell_height:
                    pg.Rect.move_ip(sprite.rect, 0, cell_height)
    # ## Update the score and print it to the console
    global score
    score += points_for_rows[cleared_rows]
    if cleared_rows > 0:
        print(f'score: {score}')


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
    # ## Every 15 ticks move currently moving block down
    if frame_counter >= 15:
        frame_counter = 0
        moving_blocks.update('d', 0)
    # ## Update the display
    screen.blit(background, (0, 0))
    moving_blocks.draw(screen)
    stationary_blocks.draw(screen)
    pg.display.flip()

