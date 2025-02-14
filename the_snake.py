from random import randint

import pygame as pg

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

# Snake speed:
SPEED = 3

# Setting up the game window:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Title for the game:
pg.display.set_caption('Snake')

# Set the time:
clock = pg.time.Clock()


class GameObject:
    """
    Base class for all game objects.
    Represents a generic game object with position and coby color.
    """

    def __init__(self, color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = color if color else None

    def draw(self):
        """
        The method is rendering the object on the game screen.
        This method is currently empty in the base class
        and should be implemented in subclasses.
        Raises:
            NotImplementedError (if this method is not implemented)
        """
        raise NotImplementedError("Subclasses must implement this method")


class Apple(GameObject):
    """
    Extends the GameObject class and represents the apple that the snake eats.
    It has a color and a position on the grid, which can be randomly assigned.
    When the snake eats an apple, its length increases by one segment.
    """

    def __init__(self, occupied_positions=None):
        if occupied_positions is None:
            occupied_positions = []
        super().__init__(APPLE_COLOR)
        self.randomize_position(occupied_positions)

    def draw(self):
        """
        This method creates a rectangular shape
        using the object's current position and size.

        The method uses `pg.draw.rect` to draw both
        the body and the border of the object.
        """
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self, occupied_positions):
        """
        Randomly assigns a new position to the object
        Args:
            occupied_positions (list): List of positions
            that are already occupied.
        """
        max_x = GRID_WIDTH - 1
        max_y = GRID_HEIGHT - 1

        while True:
            self.position = (randint(0, max_x) * GRID_SIZE,
                             randint(0, max_y) * GRID_SIZE)
            if self.position not in occupied_positions:
                break


class Snake(GameObject):
    """
    Extends the GameObject class and represents a snake.
    The snake can move in different directions,
    grow when eating apples.
    It has a dynamic position and length,
    and its movement can wrap around the screen edges.
    Colliding with the snake's own body will result in a game over.
    """

    def __init__(self):
        super().__init__(SNAKE_COLOR)
        self.positions = []
        self.last = None
        self.reset()

    def draw(self):
        """
        Iterates through the segments of the snake's body and draws
        each one as a rectangle.
        Erases the last segment of the snake's body when it moves.
        """
        # Draw snake's head:
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Erase snake's tail:
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def update_direction(self, next_direction):
        """
        Updates the snake's direction to the next direction if set.
        Resets the next direction after updating.
        """
        self.direction = next_direction

    def move(self):
        """
        Moves the snake by updating its head position
        and handling screen wrapping.
        The snake's tail is removed if its length exceeds the current size.
        """
        dx, dy = self.direction
        head_x, head_y = self.get_head_position()
        new_x = (head_x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        self.positions.insert(0, (new_x, new_y))

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
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]
        self.last = None


def handle_keys(game_object):
    """
    Listens for key events and updates the direction of the given game object
    based on user input. The direction is only updated if the new
    direction is not directly opposite to the current direction.

    Args:
        game_object (GameObject)
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                # game_object.next_direction = UP
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                # game_object.next_direction = DOWN
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                # game_object.next_direction = LEFT
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                # game_object.next_direction = RIGHT
                game_object.update_direction(RIGHT)
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def main():
    """
    Initializes the game components (snake, apple, and stone).
    Continuously runs the game loop.
    The loop handles user input, updates game objects,
    checks for collisions, and redraws the screen.
    The game runs until it is closed by the user.

    The game ends when the snake collides with itself or the stone.
    """
    pg.init()

    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position(snake.positions)
        elif snake.get_head_position() in snake.positions[2:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        apple.draw()
        snake.draw()
        snake.move()
        pg.display.update()


if __name__ == '__main__':
    main()
