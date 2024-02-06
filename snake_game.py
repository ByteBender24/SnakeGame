import pygame
import sys

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
        self.vel = 4
        self.x = 32
        self.y = 32

    def add_block(self):
        bodyblock = BodyBlock()
        if self.facing == -1:
            bodyblock.x = self.x + 32
        if self.facing == -2:
            bodyblock.y = self.y - 32
        if self.facing == +1:
            bodyblock.x = self.x - 32
        if self.facing == +2:
            bodyblock.y = self.y + 32
        self.blocks.append(bodyblock)

    def draw(self):
        WIN.blit(self.headblock, (self.x, self.y))

    # def move(self):
    #     self.


class BodyBlock:
    def __init__(self):
        self.block = pygame.image.load(r".\assets\snakebody.png")
        self.x = 32
        self.y = 32
        self.facing = 1


def draw(blocks, snake):
    WIN.fill(WHITE)
    blocks.draw()
    snake.draw()
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

    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        SNAKE.facing = -1
        SNAKE.x -= SNAKE.vel
    elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        SNAKE.facing = +1
        SNAKE.x += SNAKE.vel
    elif keys[pygame.K_UP] or keys[pygame.K_w]:
        SNAKE.facing = +2
        SNAKE.y -= SNAKE.vel
    elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
        SNAKE.facing = -2
        SNAKE.y += SNAKE.vel

    # Update body blocks' positions
    for i in range(1, len(SNAKE.blocks)):
        SNAKE.blocks[i].x = SNAKE.blocks[i-1].x
        SNAKE.blocks[i].y = SNAKE.blocks[i-1].y

BLOCK = Blocks()
SNAKE = Snake()

while True:
    handle_events()
    draw(BLOCK, SNAKE)
    movement()
    pygame.display.update()
