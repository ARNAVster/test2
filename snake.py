import pygame
import random
import pygame.font

# Initialize Pygame
pygame.init()
pygame.font.init()

font = pygame.font.SysFont('arial.ttf', 25)

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GREEN1 = (167,217,72)
GREEN2 = (142,204,57)
BLUE = (0, 0, 255)

# Define constants for the game
CELL_SIZE = 30
GRID_LENGTH_X = 16
GRID_LENGTH_Y = 16
INITIAL_LENGTH = 3
INITIAL_SPEED = 5

# Set up the screen
SCREEN_WIDTH = GRID_LENGTH_X * CELL_SIZE
SCREEN_HEIGHT = GRID_LENGTH_Y * CELL_SIZE
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

# Define the Snake class
class Snake():
    def __init__(self, x, y):
        self.segments = []
        self.direction = 'right'
        self.speed = INITIAL_SPEED
        self.score = 0
        for i in range(INITIAL_LENGTH):
            self.segments.append([x - i * CELL_SIZE, y])

    def draw(self):
        for segment in self.segments:
            pygame.draw.rect(screen, BLUE, (segment[0], segment[1], CELL_SIZE, CELL_SIZE))

    def move(self):
        # Move the snake by adding a new segment in the direction of travel
        if self.direction == 'right':
            new_segment = [self.segments[0][0] + CELL_SIZE, self.segments[0][1]]
        elif self.direction == 'left':
            new_segment = [self.segments[0][0] - CELL_SIZE, self.segments[0][1]]
        elif self.direction == 'up':
            new_segment = [self.segments[0][0], self.segments[0][1] - CELL_SIZE]
        elif self.direction == 'down':
            new_segment = [self.segments[0][0], self.segments[0][1] + CELL_SIZE]
        self.segments.insert(0, new_segment)
        self.segments.pop()

    def collide_with_food(self, food):
        # Check if the snake collides with the food
        if self.segments[0][0] == food.position[0] and self.segments[0][1] == food.position[1]:
            self.segments.append(self.segments[-1])
            self.score += 1
            return True
        return False

    def collide_with_self(self):
        # Check if the snake collides with itself
        for i in range(1, len(self.segments)):
            if self.segments[i][0] == self.segments[0][0] and self.segments[i][1] == self.segments[0][1]:
                return True
        return False

    def collide_with_wall(self):
        # Check if the snake collides with the wall
        if self.segments[0][0] < 0 or self.segments[0][0] >= SCREEN_WIDTH or \
           self.segments[0][1] < 0 or self.segments[0][1] >= SCREEN_HEIGHT:
            return True
        return False

# Define the Food class
class Food():
    def __init__(self):
        self.position = [random.randrange(0, SCREEN_WIDTH - CELL_SIZE, CELL_SIZE),
                          random.randrange(0, SCREEN_HEIGHT - CELL_SIZE, CELL_SIZE)]

    def draw(self):
        pygame.draw.rect(screen, RED, (self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))

# Initialize the game objects
snake = Snake(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
food = Food()

# Set up the game clock
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.direction != 'left':
                snake.direction = 'right'
            elif event.key == pygame.K_LEFT and snake.direction != 'right':
                snake.direction = 'left'
            elif event.key == pygame.K_UP and snake.direction != 'down':
                snake.direction = 'up'
            elif event.key == pygame.K_DOWN and snake.direction != 'up':
                snake.direction = 'down'

    for row in range(GRID_LENGTH_Y):
        for col in range(GRID_LENGTH_X):
            color = GREEN1 if (row + col) % 2 == 0 else GREEN2
            pygame.draw.rect(screen, color, pygame.Rect(col*CELL_SIZE, row*CELL_SIZE, CELL_SIZE, CELL_SIZE))
    score_text = font.render('Score: ' + str(snake.score), True, WHITE)
    screen.blit(score_text, (0, 0))

    # Draw the snake and the food
    snake.draw()
    food.draw()

    # Move the snake
    snake.move()

    # Check for collisions
    if snake.collide_with_food(food):
        food = Food()
    elif snake.collide_with_self() or snake.collide_with_wall():
        running = False

    # Update the display
    pygame.display.update()

    # Tick the clock
    clock.tick(snake.speed*2)

# Quit Pygame
pygame.quit()
