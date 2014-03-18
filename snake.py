import pygame, random
from pygame.locals import *

LEFT = K_LEFT
UP = K_UP
RIGHT = K_RIGHT
DOWN = K_DOWN

SQUARE_SIZE = 40

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

PAUSED = "paused"
RUNNING = "running"
EXIT = "exit"
YUMYUM_EATEN = "yumyum eaten"

class Snake(object):
    def __init__(self, x, y):
        self.bits = [(x, y)]
    
    def collision(self):
        return sorted(list(set(self.bits))) != sorted(self.bits)
    
    def outside(self):
        for bit in self.bits:
            if (not bit[0] in range(0, WINDOW_WIDTH / SQUARE_SIZE)) or (not bit[1] in range(0, WINDOW_HEIGHT / SQUARE_SIZE)):
                return True
    
    def update(self, state, direction, yumyum):
        if direction == LEFT:
            dx = -1
            dy = 0
        elif direction == UP:
            dx = 0
            dy = -1
        elif direction == RIGHT:
            dx = 1
            dy = 0
        elif direction == DOWN:
            dx = 0
            dy = 1
        
        self.bits.append((self.bits[-1][0] + dx, self.bits[-1][1] + dy))
        self.bits.pop(0)
        
        if self.collision() or self.outside():
            return EXIT
        
        if yumyum == self.bits[-1]:
            self.bits.insert(0, (self.bits[0][0] - dx, self.bits[0][1] - dy))
            return YUMYUM_EATEN
        
        return state
    
    def draw(self, surface):
        for bit in self.bits[:-1]:
            draw_square(surface, bit, (0, 255, 0))
        draw_square(surface, self.bits[0], (255, 255, 0))
        draw_square(surface, self.bits[-1], (255, 0, 0))

def draw_square(surface, position, color):
    pygame.draw.rect(surface, color, (position[0] * SQUARE_SIZE, position[1] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw(surface, yumyum, snake):
    surface.fill((0, 0, 0))
    
    draw_square(surface, yumyum, (255, 255, 255))
    
    snake.draw(surface)
    
    pygame.display.flip()

def update(surface, state, snake, yumyum, direction):
    if state == RUNNING:
        state = snake.update(state, direction, yumyum)
        
        draw(surface, yumyum, snake)
    elif state == PAUSED:
        pass
    elif state == YUMYUM_EATEN:
        yumyum = (random.randint(1, WINDOW_WIDTH / SQUARE_SIZE - 2), random.randint(1, WINDOW_HEIGHT / SQUARE_SIZE - 2))
        
        state = RUNNING
        
        return update(surface, state, snake, yumyum, direction)
    
    return state, snake, yumyum

def main():
    pygame.init()
    
    surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    
    state = RUNNING
    direction = RIGHT
    
    snake = Snake(0, 0)
    
    clock = pygame.time.Clock()
    
    yumyum = (5, 5)
    
    while state != EXIT:
        for event in pygame.event.get():
            if event.type == QUIT:
                state = EXIT
            elif event.type == KEYDOWN:
                if event.key in [UP, DOWN, LEFT, RIGHT]:
                    direction = event.key
                elif event.key == K_ESCAPE:
                    if state == PAUSED:
                        state = RUNNING
                    else:
                        state = PAUSED
        
        clock.tick(10)
        
        state, snake, yumyum = update(surface, state, snake, yumyum, direction)
    
    pygame.quit()

if __name__ == "__main__":
    main()
