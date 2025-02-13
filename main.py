import pygame
import sys
import random

pygame.init()

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 700
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

FOOD_COLOR = (255, 255, 0)
LIGHT_TURQUOISE = (64, 224, 208)
DARK_TURQUOISE = (0, 206, 209)

UP = (0, -1)
DOWN = (0, 1)
RIGHT = (1, 0)
LEFT = (-1, 0)

SNAKE_SPEED = 15

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("Snake Game")
icon = pygame.image.load('snake.png')
pygame.display.set_icon(icon)

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, RIGHT, LEFT])
        self.length = 1
        self.score = 0

    def draw(self, surface):
        counter = 0
        for p in self.positions:
            blue = max(30, 163 - (counter * 5))
            color = (0, 35, blue)
            pygame.draw.rect(surface, color, (p[0] * GRID_SIZE, p[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))
            counter += 1

    def move(self):
        current = self.positions[0]
        x, y = self.direction

        new_x = current[0] + x
        new_y = current[1] + y

        hit_wall = new_x < 0 or new_x >= GRID_WIDTH or new_y < 0 or new_y >= GRID_HEIGHT
        new = (new_x, new_y)
        hit_self = new in self.positions[3:]

        if hit_wall or hit_self:
            self.reset()  # Reset snake position and score
        else:
            self.positions.insert(0, new)

        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, RIGHT, LEFT])
        self.score = 0

class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    def draw(self, surface):
        pygame.draw.rect(surface, FOOD_COLOR,
                         (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))

def draw_grid(surface):
    for y in range(0, WINDOW_HEIGHT, GRID_SIZE):
        for x in range(0, WINDOW_WIDTH, GRID_SIZE):
            r = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            if (x // GRID_SIZE + y // GRID_SIZE) % 2 == 0:
                pygame.draw.rect(surface, LIGHT_TURQUOISE, r)
            else:
                pygame.draw.rect(surface, DARK_TURQUOISE, r)

def main():
    snake = Snake()
    food = Food()

    font = pygame.font.Font("PressStart2P-Regular.ttf", 20)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT

        snake.move()

        if snake.positions[0] == food.position:
            snake.length += 1
            snake.score += 10
            food.randomize_position()

        while food.position in snake.positions:
            food.randomize_position()

        draw_grid(screen)
        snake.draw(screen)
        food.draw(screen)

        score_text = font.render(f"Score: {snake.score}", True, (0, 0, 0))
        screen.blit(score_text, (20, 20))

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

if __name__ == "__main__":
    main()
