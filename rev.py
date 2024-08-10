import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Bird settings
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
bird_x = 50
bird_y = SCREEN_HEIGHT // 2
bird_velocity = 0
gravity = 0.5
jump_strength = -10

# Pipe settings
PIPE_WIDTH = 60
PIPE_GAP = 150
pipe_velocity = -4
pipe_frequency = 1500  # Milliseconds

# Game settings
clock = pygame.time.Clock()
score = 0
font = pygame.font.SysFont(None, 55)

# Create the pipes
def create_pipe():
    height = random.randint(100, 400)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, height + PIPE_GAP // 2, PIPE_WIDTH, SCREEN_HEIGHT - height)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, height - PIPE_GAP // 2)
    return top_pipe, bottom_pipe

# Draw the pipes
def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(SCREEN, GREEN, pipe)

# Main game loop
def main():
    global bird_y, bird_velocity, score

    pipes = []
    pygame.time.set_timer(pygame.USEREVENT, pipe_frequency)
    
    running = True
    while running:
        SCREEN.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = jump_strength
            if event.type == pygame.USEREVENT:
                pipes.append(create_pipe())

        # Bird movement
        bird_velocity += gravity
        bird_y += bird_velocity
        
        bird_rect = pygame.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
        pygame.draw.rect(SCREEN, GREEN, bird_rect)

        # Pipe movement
        for pipe_pair in pipes:
            pipe_pair[0].x += pipe_velocity
            pipe_pair[1].x += pipe_velocity

        # Remove pipes out of the screen
        pipes = [pipe_pair for pipe_pair in pipes if pipe_pair[0].x + PIPE_WIDTH > 0]

        # Draw pipes
        draw_pipes([pipe for pair in pipes for pipe in pair])

        # Check for collisions
        if bird_y > SCREEN_HEIGHT or bird_y < 0 or any(bird_rect.colliderect(pipe) for pair in pipes for pipe in pair):
            running = False

        # Scoring
        for pipe_pair in pipes:
            if pipe_pair[0].x + PIPE_WIDTH // 2 == bird_x:
                score += 1

        # Display score
        score_text = font.render(str(score), True, GREEN)
        SCREEN.blit(score_text, (SCREEN_WIDTH // 2, 20))

        # Update the display
        pygame.display.update()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
