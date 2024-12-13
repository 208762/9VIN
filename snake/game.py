import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

class Direction(Enum):
    RIGHT, LEFT, UP, DOWN = 1, 2, 3, 4
    
Point = namedtuple('Point', 'x, y')

WHITE, RED, BLUE1, BLUE2, BLACK = (255, 255, 255), (200,0,0), (0, 0, 255), (0, 100, 255), (0,0,0)

BLOCK_SIZE = 20
SPEED = 200

class SnakeGameAI:
    
    def __init__(self, w=640, h=480):
        self.width = w
        self.height = h
        
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        
    def reset(self):
        self.direction = Direction.RIGHT
        
        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(3*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0    

    def _place_food(self):
        x = random.randint(0, (self.width-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.height-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self, action):
        self.frame_iteration += 1
        print(self.frame_iteration)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        self._move(action) 
        self.snake.insert(0, self.head)
        
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake): 
            game_over = True
            reward = -10
            return reward, game_over, self.score
        
        if self.head == self.food:
            self.score += 1
            if self.frame_iteration < 50:
                reward = 10
            elif 50 < self.frame_iteration < 100:
                reward = 5
            elif self.frame_iteration > 100:
                reward = 1
            self._place_food()
        else:
            self.snake.pop()
    
        self._update_ui()
        self.clock.tick(SPEED)
            
        return reward, game_over, self.score
        
    def is_collision(self, point = None):
        if point is None:
            point = self.head
        if point.x > self.width - BLOCK_SIZE or point.x < 0 or point.y > self.height - BLOCK_SIZE or point.y < 0:
            return True
        if point in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, action):
        
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        current_direction_index = clock_wise.index(self.direction)

        if numpy.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[current_direction_index] # no change
        elif numpy.array_equal(action, [0, 1, 0]):
            next_current_direction_index = (current_direction_index + 1) % 4
            new_dir = clock_wise[next_current_direction_index]
        elif numpy.array_equal(action, [0, 0, 1]):
            next_current_direction_index = (current_direction_index - 1) % 4
            new_dir = clock_wise[next_current_direction_index]
        
        self.direction = new_dir
        
        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)