import pygame
import sys
import random

pygame.init()

WIN_WIDTH = 800
WIN_HEIGHT = 800

WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Snake Game")

# COLORS:
RED = (255, 0, 0)
WHITE = (255, 255, 255)


class Blocks:
    def __init__(self):
        self.blockbasic = pygame.image.load(r".\assets\wall_block_32_0.png")

    def draw(self):
        x, y = 0, 0

        while x < 740:
            # print(x+32, 740)
            WIN.blit(self.blockbasic, (x, y))
            x += 32
        # print("DRAWN UP BLOCKS---\n")

        while y < 740:
            # print(y+32, 740)
            WIN.blit(self.blockbasic, (x, y))
            y += 32
        # print("DRAWN RIGHT BLOCKS---n")

        while x > 0:
            # print(x-32, 740)
            WIN.blit(self.blockbasic, (x, y))
            x -= 32
        # print("DRAWN DOWN BLOCKS---\n")

        while y > 0:
            # print(y-32, 740)
            WIN.blit(self.blockbasic, (x, y))
            y -= 32
        # print("DRAWN LEFT BLOCKS---\n")


class Snake:
    '''
    blocks : list of blocks of snake
    facing : 
        -1 left
        +1 right
        -2 down
        +2 up
    '''

    def __init__(self):
        self.headblock = pygame.image.load(r".\assets\snake_green_head_64.png")
        self.blocks = [self.headblock]
        self.facing = 1
        self.vel = 32
        self.x = 32
        self.y = 32
        self.prev_coord = [self.x, self.y]
        self.size = 32

    def add_block(self):
        bodyblock = BodyBlock()
        if self.facing == -1:
            bodyblock.x = self.x + self.size
            bodyblock.y = self.y
        if self.facing == -2:
            bodyblock.y = self.y - self.size
            bodyblock.x = self.x
        if self.facing == +1:
            bodyblock.x = self.x - self.size
            bodyblock.y = self.y
        if self.facing == +2:
            bodyblock.y = self.y + self.size
            bodyblock.x = self.x
        self.blocks.append(bodyblock)

    def draw(self):
        WIN.blit(self.headblock, (self.x, self.y))
        if self.blocks:
            for num in range(1, len(self.blocks)):
                block = self.blocks[num]
                block.draw()

    def move(self):
        if self.facing == -1:
            self.prev_coord[0] = self.x
            self.x = self.x - self.vel
        if self.facing == -2:
            self.prev_coord[1] = self.y
            self.y = self.y + self.vel
        if self.facing == +1:
            self.prev_coord[0] = self.x
            self.x = self.x + self.vel
        if self.facing == +2:
            self.prev_coord[1] = self.y
            self.y = self.y - self.vel

    def get_hitbox(self, part="head"):
        '''To check collisions and stuff (returns the draw rectangle around sprites)'''
        if part == "head":
            return pygame.Rect(self.x, self.y, 64, 64)


class BodyBlock:
    def __init__(self):
        self.block = pygame.image.load(r".\assets\snakebody.png")
        self.x = 32
        self.y = 32
        self.prev_coord = [self.x, self.y]
        self.facing = 1

    def get_hitbox(self):
        '''To check collisions and stuff (returns the draw rectangle around sprites)'''
        return pygame.Rect(self.x + 17, self.y + 11, 29, 52)

    def draw(self):
        WIN.blit(self.block, (self.x, self.y))

    def move(self):
        if self.facing == -1:
            self.prev_coord[0] = self.x
            self.x = self.x - self.vel
        if self.facing == -2:
            self.prev_coord[1] = self.y
            self.y = self.y + self.vel
        if self.facing == +1:
            self.prev_coord[0] = self.x
            self.x = self.x + self.vel
        if self.facing == +2:
            self.prev_coord[1] = self.y
            self.y = self.y - self.vel


class Food:
    def __init__(self):
        self.food = pygame.image.load(r".\assets\apple_alt_64.png")
        # 32 is excluding the width of borders
        self.x = random.randint(32, WIN_WIDTH-96)
        self.y = random.randint(32, WIN_HEIGHT-96)

    def draw(self):
        WIN.blit(self.food, (self.x, self.y))

    def get_hitbox(self):
        '''To check collisions and stuff (returns the draw rectangle around sprites)'''
        return pygame.Rect(self.x, self.y+8, 64, 56)


def draw(blocks, snake, apple):
    WIN.fill(WHITE)
    blocks.draw()
    snake.draw()
    if apple is not None:
        apple.draw()
        pygame.draw.rect(WIN, (255, 0, 0), apple.get_hitbox(), 2)
    pygame.draw.rect(WIN, (255, 0, 0), snake.get_hitbox(), 2)
    pygame.display.update()


def handle_events():
    '''
    Essential for handling quits and handling crashes in windows systems
    '''

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def movement():
    keys = pygame.key.get_pressed()

    if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and SNAKE.facing != 1:
        SNAKE.facing = -1

    elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and SNAKE.facing != -1:
        SNAKE.facing = +1

    elif (keys[pygame.K_UP] or keys[pygame.K_w]) and SNAKE.facing != -2:
        SNAKE.facing = +2

    elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and SNAKE.facing != 2:
        SNAKE.facing = -2

    for i in range(1, len(SNAKE.blocks)):
        if isinstance(SNAKE.blocks[i-1], pygame.surface.Surface):
            x = SNAKE.prev_coord[0]
            y = SNAKE.prev_coord[1]
            SNAKE.blocks[i].x = x
            SNAKE.blocks[i].y = y
            SNAKE.blocks[i].facing = SNAKE.facing
        else:
            SNAKE.blocks[i].x = SNAKE.blocks[i-1].prev_coord[0]
            SNAKE.blocks[i].y = SNAKE.blocks[i-1].prev_coord[1]
            SNAKE.blocks[i].facing = SNAKE.blocks[i-1].facing


def random_apple_generator():
    global APPLE

    if APPLE is None:
        apple = Food()
        APPLE = apple


def collision_check(block, snake):
    global APPLE
    if APPLE.get_hitbox().colliderect(snake.get_hitbox("head")):
        APPLE = None
        snake.add_block()


CLOCK = pygame.time.Clock()
APPLE = Food()
BLOCK = Blocks()
SNAKE = Snake()

while True:
    CLOCK.tick(5)
    handle_events()
    SNAKE.move()
    draw(BLOCK, SNAKE, APPLE)
    collision_check(BLOCK, SNAKE)
    movement()
    random_apple_generator()
    pygame.display.update()
