# Czy lepiej zrobić tak, że stan gry będzie źródłem wiedzy na temat tego, co na ekranie?
# pyUnit - do testowania, może jest jakiś dedykowany pygamowi, nawet jeśli nie ma CD to CI w testach ma sens
# baza danych KURSORY
# SQL injection - bindowanie żeby zabezpieczyć

# Integracja pyCharm - git
# Zrobienie tego online - obgadane
# CI / CD
# praca na repo - branche, updaty itede

import pygame as pg
import os
import random
if not pg.font:
    print('Warning: fonts disabled')
if not pg.mixer:
    print('Warning: sound disabled')

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')

no_of_rows = 12
no_of_columns = 16
# CZEMU TO NIE DZIALA???
# game_state = [[False]*no_of_rows]*no_of_columns

# zamienić tablicę kolumn na tablicę wierszy i pozostałe rzeczy dostosować
game_state = []
for i in range(0, no_of_columns):
    column = []
    for j in range(0, no_of_rows):
        column.append(False)
    game_state.append(column)

# TYLKO DO DEBUGOWANIA
def print_game_state_pretty():
    for j in range(no_of_rows):
        row_s = ""
        separator = "_____________________________________________________________"
        for column in game_state:
            if column[j]:
                row_s += 'X\t'
            else:
                row_s += '.\t'
        print(row_s)
        if j == no_of_rows - 1:
            print(separator)

class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Block(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.add(moving_blocks)
        self.position = Position(6, 0)
        self.fields = []
        self.rotation = 0
        game_window = pg.Surface(screen.get_size())
        self.cell_width = game_window.get_width() / no_of_columns
        self.cell_height = game_window.get_height() / no_of_rows

    def _draw(self):
        self.image = pg.Surface((3 * self.cell_width, 3 * self.cell_height))
        self.image.fill((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.position.x * self.cell_width, self.position.y * self.cell_height)
        for field in self.fields:
            field_surface = pg.Surface((self.cell_width, self.cell_height))
            field_surface.fill((0, 0, 0))
            dest = (
                (field.x - self.position.x) * self.cell_width,
                (field.y - self.position.y) * self.cell_height
            )
            self.image.blit(field_surface, dest)

    def _stop(self):
        self.remove(moving_blocks)
        self.add(stationary_blocks)
        new_block()

    # ZDECYDOWAC CZY move CZY RACZEJ _move
    def move(self, direction, rotation):
        if len(self.fields) == 0:
            print('Error! This block has no fields (self.fields has length 0)!')
            return
        else:
            # oblicz nowy obrót od którego zaczniesz obliczać pola
            new_rotation = (self.rotation + rotation) % 360
            # oblicz, jeżeli został wskazany kierunek, nową pozycję od której zaczniesz obliczać zajęte pola
            new_position = self.position
            if direction == 'l':
                new_position = Position(self.position.x - 1, self.position.y)
            if direction == 'r':
                new_position = Position(self.position.x + 1, self.position.y)
            if direction == 'd':
                new_position = Position(self.position.x, self.position.y + 1)
            # usuń klocek z tablicy stanu gry
            for field in self.fields:
                game_state[field.x][field.y] = False
            # oblicz pola zajmowane przez klocek po ruchu
            new_fields = self.calculate_fields(new_position.x, new_position.y, new_rotation)
            # sprawdź, czy którekolwiek z obliczonych wyżej pól jest już zajęte lub jest poza granicą
            collision_horizontal = False
            collision_vertical = False
            for field in new_fields:
                # trzeba najpierw sprawdzić, czy klocek nie wychodzi poza planszę i dopiero po upewnieniu się, że nie,
                # można sprawdzać czy koliduje z innym klockiem na planszy
                if field.y > no_of_rows - 1:
                    collision_vertical = True
                    break
                if field.x > no_of_columns - 1 or field.x < 0:
                    collision_horizontal = True
                    break
                # sprawdzanie czy pola stanu gry nie są już zajęte może nastąpić dopiero po upewnieniu się,
                # że nowe pola klocka nie są poza granicami planszy
                if game_state[field.x][field.y]:
                    if direction in ('l', 'r'):
                        collision_horizontal = True
                    if direction == 'd':
                        collision_vertical = True
            # jeśli występuje kolizja pionowo, zatrzymaj klocek
            if collision_vertical:
                self._stop()
            # jeśli nie występuje kolizja pionowa ani pozioma, zmień pozycję klocka i zaktualizuj zajmowane przez klocek pola
            elif not collision_horizontal:
                self.position = new_position
                self.fields = new_fields
                self.rotation = new_rotation
            for field in self.fields:
                game_state[field.x][field.y] = True

    def update(self, direction, rotation):
        self.move(direction, rotation)
        self._draw()

    def calculate_fields(self, x, y):
        print("Error! calculate_fields class must be defined in a child class")
        return


class Square_Block(Block):
    def __init__(self):
        super().__init__()
        self.fields = self.calculate_fields(self.position.x, self.position.y, self.rotation)

    def calculate_fields(self, x, y, rotation):
        new_fields = [
            Position(x, y),
            Position(x + 1, y),
            Position(x, y + 1),
            Position(x + 1, y + 1)
        ]
        return new_fields


class L_Block(Block):
    def __init__(self):
        super().__init__()
        self.fields = self.calculate_fields(self.position.x, self.position.y, self.rotation)

    def calculate_fields(self, x, y, rotation):
        if rotation == 0:
            new_fields = [
                Position(x, y),
                Position(x, y + 1),
                Position(x, y + 2),
                Position(x + 1, y + 2)
            ]
        if rotation == 90:
            new_fields = [
                Position(x, y + 1),
                Position(x, y),
                Position(x + 1, y),
                Position(x + 2, y)
            ]
        if rotation == 180:
            new_fields = [
                Position(x, y),
                Position(x + 1, y),
                Position(x + 1, y + 1),
                Position(x + 1, y + 2)
            ]
        if rotation == 270:
            new_fields = [
                Position(x, y + 1),
                Position(x + 1, y + 1),
                Position(x + 2, y + 1),
                Position(x + 2, y)
            ]
        return new_fields


class Line_Block(Block):
    def __init__(self):
        super().__init__()
        self.fields = self.calculate_fields(self.position.x, self.position.y, self.rotation)

    def calculate_fields(self, x, y, rotation):
        if rotation in (0, 180):
            new_fields = [
                Position(x, y),
                Position(x, y + 1),
                Position(x, y + 2),
            ]
        elif rotation in (90, 270):
            new_fields = [
                Position(x, y + 1),
                Position(x + 1, y + 1),
                Position(x + 2, y + 1),
            ]
        return new_fields


class Diagonal_Block(Block):
    def __init__(self):
        super().__init__()
        self.fields = self.calculate_fields(self.position.x, self.position.y, self.rotation)

    def calculate_fields(self, x, y, rotation):
        if rotation in (0, 180):
            new_fields = [
                Position(x, y),
                Position(x, y + 1),
                Position(x + 1, y + 1),
                Position(x + 1, y + 2)
            ]
        elif rotation in (90, 270):
            new_fields = [
                Position(x, y + 1),
                Position(x + 1, y + 1),
                Position(x + 1, y),
                Position(x + 2, y)
            ]
        return new_fields


def new_block():
    random.seed()
    rand_int = random.randrange(0, 4)
    if rand_int == 0:
        Square_Block()
    elif rand_int == 1:
        L_Block()
    elif rand_int == 2:
        Line_Block()
    elif rand_int == 3:
        Diagonal_Block()
    moving_blocks.update('d', 0)
    moving_blocks.draw(screen)
    stationary_blocks.draw(screen)
    pg.display.flip()


def check_and_clear():
    # JAK MOŻNA TO LEPIEJ ZROBIC, BARDZIEJ PYTHONOWO
    # calculate cell height
    game_window = pg.Surface(screen.get_size())
    cell_height = game_window.get_height() / no_of_rows
    # for each row, calculate if it is full; if it is, remove the row from game state and from the screen, then
    # update all cells above the deleted row so they fall into emptied space both on screen and in game state
    for j in range(no_of_rows):
        row_full = True
        for column in game_state:
            if not column[j]:
                row_full = False
                break
        if row_full:
            for column in game_state:
                for j_2 in range(j, -1, -1):
                    if j_2 > 0:
                        column[j_2] = column[j_2 - 1]
                    else:
                        column[j_2] = False
            print('row is full')
            for sprite in stationary_blocks.sprites():
                rect = sprite.rect
                rect.move_ip(0, cell_height)

# To jakoś ładnie pogrupować i opisać
running = True
pg.init()
frame_clock = pg.time.Clock()
screen = pg.display.set_mode((640, 480))
background = pg.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))
screen.blit(background, (0, 0))
pg.display.flip()
moving_blocks = pg.sprite.Group()
stationary_blocks = pg.sprite.Group()
new_block()
frame_counter = 0
i = 0
while running:
    frame_clock.tick(30)
    frame_counter += 1
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
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
        elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
            running = False
    if frame_counter >= 15:
        frame_counter = 0
        check_and_clear()
        moving_blocks.update('d', 0)
        print_game_state_pretty()
    screen.blit(background, (0, 0))
    moving_blocks.draw(screen)
    stationary_blocks.draw(screen)
    pg.display.flip()

