from random import randint

import pygame

# Constants for field and grid sizes:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Movements directions:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Background color:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Cell border color:
BORDER_COLOR = (93, 216, 228)

# Apple color:
APPLE_COLOR = (255, 0, 0)

# Snake color:
SNAKE_COLOR = (0, 255, 0)

# Stone color:
# STONE_COLOR = (128, 128, 128)

# Snake speed:
SPEED = 3

# Setting up the game window:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Title for the game:
pygame.display.set_caption('Snake')

# Set the time:
clock = pygame.time.Clock()


class GameObject:
    """
    Base class for all game objects.
    Represents a generic game object with position and coby color.
    """

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """
        The method is rendering the object on the game screen.
        This method is currently empty in the base class
        and should be implemented in subclasses.
        """
        pass


class Apple(GameObject):
    """
    Extends the GameObject class and represents the apple that the snake eats.
    It has a color and a position on the grid, which can be randomly assigned.
    When the snake eats an apple, its length increases by one segment.
    """

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def draw(self):
        """
        This method creates a rectangular shape
        using the object's current position and size.

        The method uses `pygame.draw.rect` to draw both
        the body and the border of the object.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Randomly assigns a new position to the object"""
        max_x = GRID_WIDTH - 1
        max_y = GRID_HEIGHT - 1

        x = randint(0, max_x) * GRID_SIZE
        y = randint(0, max_y) * GRID_SIZE

        self.position = x, y

# class Stone(GameObject):
#     """
#     Extends the GameObject class and represents a stone
#     that the snake may collide with.
#     The stone has a fixed position and does not move.
#     Colliding with the stone may result in the snake's game over.
#     """
#
#     def __init__(self, occupied_positions=None):
#         super().__init__()
#         self.body_color = STONE_COLOR
#         self.randomize_position(occupied_positions)
#
#     def draw(self):
#         """
#         This method creates a rectangular shape
#         using the object's current position and size.
#
#         The method uses `pygame.draw.rect` to draw both
#         the body and the border of the object.
#         """
#         rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Extends the GameObject class and represents a snake.
    The snake can move in different directions,
    grow when eating apples, and check for self-collisions.
    It has a dynamic position and length,
    and its movement can wrap around the screen edges.
    Colliding with the snake's own body will result in a game over.
    """

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.last = None

    def draw(self):
        """
        Iterates through the segments of the snake's body and draws
        each one as a rectangle.
        Erases the last segment of the snake's body when it moves.
        """
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Draw snake's head:
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Erase snake's tail:
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self):
        """
        Updates the snake's direction to the next direction if set.
        Resets the next direction after updating.
        """
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def handle_wrapping(self, step):
        """
        Wraps the position around the screen boundaries.
        If the snake moves off-screen, it reappears on the opposite edge.
        """
        x, y = step
        if x >= SCREEN_WIDTH:
            x = 0
        elif x < 0:
            x = SCREEN_WIDTH

        if y >= SCREEN_HEIGHT:
            y = 0
        elif y < 0:
            y = SCREEN_HEIGHT
        return x, y

    def move(self):
        """
        Moves the snake by updating its head position
        and handling screen wrapping.
        The snake's tail is removed if its length exceeds the current size.
        """
        self.update_direction()

        start = self.get_head_position()
        direction = (self.direction[0] * GRID_SIZE,
                     self.direction[1] * GRID_SIZE)
        step = tuple(a + b for a, b in zip(start, direction))
        self.positions = [self.handle_wrapping(step)] + self.positions

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def get_head_position(self):
        """Returns the current position of the snake's head."""
        return self.positions[0]

    def reset(self):
        """
        Resets the snake to its initial state, clearing its previous position
        and setting its length, direction, and position back
        to the starting point.
        """
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.last = None

    def is_collision(self):
        """
        Checks if the snake's head has collided with any part of its body.
        Returns:
            bool: True if a collision is detected, otherwise False.
        """
        for segment in self.positions[2:]:
            if segment == self.get_head_position():
                return True
        return False


def handle_keys(game_object):
    """
    Listens for key events and updates the direction of the given game object
    based on user input. The direction is only updated if the new
    direction is not directly opposite to the current direction.

    Args:
        game_object (GameObject)
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """
    Initializes the game components (snake, apple, and stone).
    Continuously runs the game loop.
    The loop handles user input, updates game objects,
    checks for collisions, and redraws the screen.
    The game runs until it is closed by the user.

    The game ends when the snake collides with itself or the stone.
    """
    pygame.init()

    snake = Snake()
    apple = Apple()
    # stone = Stone([snake.positions, apple.position])

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        apple.draw()
        # stone.draw()
        snake.draw()
        snake.move()

        if apple.position == snake.get_head_position():
            snake.length += 1
            snake.positions.append(snake.positions[-1])
            apple.randomize_position([snake.positions])

        # if snake.is_collision() or stone.position == snake.get_head_position():
        if snake.is_collision():
            snake.reset()

        pygame.display.update()


if __name__ == '__main__':
    main()
