import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Bird properties
bird_width = 40
bird_height = 30
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0

# Pipe properties
pipe_width = 50
pipe_gap = 150
pipe_velocity = 3
pipes = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Load images
bird_image = pygame.image.load("flappybird.jpeg")
bird_image = pygame.transform.scale(bird_image, (bird_width, bird_height))
pipe_image = pygame.Surface((pipe_width, SCREEN_HEIGHT))
pipe_image.fill((0, 255, 0))

# Main game loop
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_velocity = -7

    # Update bird position
    bird_velocity += 0.5
    bird_y += bird_velocity

    # Generate pipes
    if len(pipes) == 0 or pipes[-1]["x"] < SCREEN_WIDTH - 200:
        pipe_height = random.randint(50, 350)
        pipes.append({"x": SCREEN_WIDTH, "y": pipe_height})

    # Move pipes
    for pipe in pipes:
        pipe["x"] -= pipe_velocity

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe["x"] > -pipe_width]

    # Collision detection
    bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
    for pipe in pipes:
        pipe_rect_upper = pygame.Rect(pipe["x"], 0, pipe_width, pipe["y"])
        pipe_rect_lower = pygame.Rect(pipe["x"], pipe["y"] + pipe_gap, pipe_width, SCREEN_HEIGHT - pipe["y"] - pipe_gap)
        if bird_rect.colliderect(pipe_rect_upper) or bird_rect.colliderect(pipe_rect_lower) or bird_y > SCREEN_HEIGHT:
            running = False

    # Score increment
    for pipe in pipes:
        if pipe["x"] + pipe_width < bird_x and not pipe.get("counted", False):
            score += 1
            pipe["counted"] = True

    # Clear the screen
    screen.fill(WHITE)

    # Draw pipes
    for pipe in pipes:
        upper_pipe_y = pipe["y"] - pipe_image.get_height()
        lower_pipe_y = pipe["y"] + pipe_gap
        screen.blit(pipe_image, (pipe["x"], upper_pipe_y))  # Upper pipe
        screen.blit(pipe_image, (pipe["x"], lower_pipe_y))  # Lower pipe

    # Draw bird
    screen.blit(bird_image, (bird_x, bird_y))

    # Display score
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.update()

    # Tick
    clock.tick(30)

# Game over
pygame.quit()
