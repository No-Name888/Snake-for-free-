import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
LIGHT_GREEN = (100, 255, 100)  # Lighter green for hover effect
RED = (255, 0, 0)
BLACK = (0, 0, 0)
SNAKE_SIZE = 10
FPS = 12  # Start with 12 FPS

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Set up the clock
clock = pygame.time.Clock()


def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], SNAKE_SIZE, SNAKE_SIZE))


def generate_food():
    x = random.randint(0, (WIDTH - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    y = random.randint(0, (HEIGHT - SNAKE_SIZE) // SNAKE_SIZE) * SNAKE_SIZE
    return x, y


def show_menu():
    font = pygame.font.Font(None, 74)
    button_font = pygame.font.Font(None, 36)
    start_text = button_font.render("START", True, BLACK)

    # Center the button
    button_width, button_height = 200, 100
    button_rect = pygame.Rect((WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height // 2),
                              (button_width, button_height))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if button_rect.collidepoint(event.pos):
                        return  # Start the game if the button is clicked

        # Fill the menu background with black
        screen.fill(BLACK)

        # Check if the mouse is over the button
        if button_rect.collidepoint(pygame.mouse.get_pos()):
            button_color = LIGHT_GREEN  # Change to lighter green on hover
        else:
            button_color = GREEN  # Normal color

        pygame.draw.rect(screen, button_color, button_rect)  # Draw the button

        # Center the text in the button
        text_rect = start_text.get_rect(center=button_rect.center)
        screen.blit(start_text, text_rect)

        pygame.display.flip()
        clock.tick(60)


def main():
    # Game variables
    snake = [(100, 100), (90, 100), (80, 100)]
    direction = (SNAKE_SIZE, 0)  # Moving right
    food_position = generate_food()
    score = 0
    current_fps = FPS  # Set initial FPS

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (0, SNAKE_SIZE):
                    direction = (0, -SNAKE_SIZE)
                elif event.key == pygame.K_DOWN and direction != (0, -SNAKE_SIZE):
                    direction = (0, SNAKE_SIZE)
                elif event.key == pygame.K_LEFT and direction != (SNAKE_SIZE, 0):
                    direction = (-SNAKE_SIZE, 0)
                elif event.key == pygame.K_RIGHT and direction != (-SNAKE_SIZE, 0):
                    direction = (SNAKE_SIZE, 0)

        # Move the snake
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Check for collision with walls
        if (new_head[0] < 0 or new_head[0] >= WIDTH or
                new_head[1] < 0 or new_head[1] >= HEIGHT or
                new_head in snake):
            print(f"Game Over! Your score: {score}")
            pygame.quit()
            sys.exit()

        # Add the new head to the snake
        snake.insert(0, new_head)

        # Check for food collision
        if new_head == food_position:
            score += 1
            current_fps += 1  # Increase FPS by 1
            food_position = generate_food()
        else:
            snake.pop()  # Remove the last segment

        # Draw everything
        screen.fill(BLACK)
        draw_snake(snake)
        pygame.draw.rect(screen, RED, pygame.Rect(food_position[0], food_position[1], SNAKE_SIZE, SNAKE_SIZE))

        pygame.display.flip()
        clock.tick(current_fps)  # Use the current FPS


if __name__ == "__main__":
    while True:
        show_menu()  # Show the menu
        main()  # Start the game

