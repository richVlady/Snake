import pygame, sys, random
from pygame.math import Vector2

class FRUIT:
    def __init__(self):
        self.randomize()
    def draw_fruit(self):
        x = int(self.pos.x * cellSize)
        y = int(self.pos.y * cellSize)
        fruit_rect = pygame.Rect(x, y, cellSize, cellSize)
        screen.blit(apple,fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cellNum - 1)
        self.y = random.randint(0, cellNum - 1)
        self.pos = Vector2(self.x, self.y)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(7,10), Vector2(8,10), Vector2(9,10)]
        self.direction = Vector2(-1,0)
        self.new_block = False

    def draw_snake(self):
        for index,block in enumerate(self.body):
            x = int(block.x * cellSize)
            y = int(block.y * cellSize)
            block_rect = pygame.Rect(x,y,cellSize,cellSize)

            if index == 0:
                if self.direction == Vector2(1,0):
                    screen.blit(head_right,block_rect)
                elif self.direction == Vector2(-1,0):
                    screen.blit(head_left,block_rect)
                elif self.direction == Vector2(0,-1):
                    screen.blit(head_up,block_rect)
                else:
                    screen.blit(head_down,block_rect)

            elif index == (len(self.body)-1):
                if self.body[-2].x == self.body[-1].x-1:
                    screen.blit(tail_right,block_rect)
                elif self.body[-2].x == self.body[-1].x+1:
                    screen.blit(tail_left,block_rect)
                elif self.body[-2].y == self.body[-1].y-1:
                    screen.blit(tail_down,block_rect)
                else:
                    screen.blit(tail_up,block_rect)

            elif self.body[index-1].x == block.x == self.body[index+1].x:
                screen.blit(body_vertical,block_rect)
            elif self.body[index-1].y == block.y == self.body[index+1].y:
                screen.blit(body_horizontal,block_rect)

            else:
                if self.body[index-1].y < self.body[index+1].y: #going up
                    if self.body[index-1].x < self.body[index+1].x: # going left
                        if block.x == self.body[index-1].x: # hori
                            screen.blit(body_tr, block_rect)
                        else: # vert
                            screen.blit(body_bl, block_rect)
                    else:
                        if block.x == self.body[index-1].x:
                            screen.blit(body_tl, block_rect)
                        else:
                            screen.blit(body_br, block_rect)
                else: # going down
                    if self.body[index - 1].x < self.body[index + 1].x:  # going left
                        if block.x == self.body[index - 1].x:  # hori
                            screen.blit(body_br, block_rect)
                        else:
                            screen.blit(body_tl, block_rect)
                    else: # going right
                        if block.x == self.body[index - 1].x:  # hori
                            screen.blit(body_bl, block_rect)
                        else:
                            screen.blit(body_tr, block_rect)


    def move_snake(self):
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0,body_copy[0] + self.direction)
            self.body = body_copy

    def add_block(self):
        self.new_block = True

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cellNum or not 0 <= self.snake.body[0].y < cellNum:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def draw_grass(self):
        grass_color = (127,209,51)

        for row in range(cellNum):
            for col in range(cellNum):
                x = row * cellSize
                y = col * cellSize
                grass_rect = pygame.Rect(x,y,cellSize,cellSize)
                if ((col + row)%2 == 1):
                    pygame.draw.rect(screen,grass_color,grass_rect)

    def game_over(self):
        pygame.quit()
        sys.exit()

pygame.init()
cellSize = 40
cellNum = 20
screen = pygame.display.set_mode((cellSize * cellNum,cellSize * cellNum))
clock = pygame.time.Clock()

apple = pygame.image.load('Graphics/apple.png').convert_alpha()

body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()
body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()

head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()
head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()

tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()
tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()


main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE,100)

while True:
    for event in pygame.event.get():
        snake = main_game.snake
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    snake.direction = Vector2(0,-1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    snake.direction = Vector2(0,1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    snake.direction = Vector2(-1,0)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    snake.direction = Vector2(1,0)

        screen.fill((175,215,70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)
