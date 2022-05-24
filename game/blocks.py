block_names = [
    {
        'name': 'Square_Block'
        'constructor':
    }
]

# Abstract class laying groundwork for each type of block in the game
class Block(pg.sprite.Sprite):
    # Initialize key properties used by this class and by child classes
    def __init__(self, position, rotation, color):
        pg.sprite.Sprite.__init__(self)
        self.color = color
        self.position = position
        self.fields = []
        self.rotation = rotation
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
        new_block = game_state.get_next_block()
        game_display.moving_blocks.add(new_block)

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

