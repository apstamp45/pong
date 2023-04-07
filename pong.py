import os

# Disable pygame init message
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import pygame

# Initialize pygame
pygame.init()

starting_speed = 1.0

# Set the window size
window_width = 800
window_height = 600

# Create the window
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Pong')

# Initialize the colors
BLACK = (40, 40, 40)
WHITE = (235, 219, 210)

# Initialize the paddles
pad_width = 10
pad_height = 50
pad_speed = 2


# Initialize the ball
ball_size = 20
ball_rad = ball_size / 2

def speed(x: float):
    global ball_speed
    ball_speed = 3.0 - 3.0 / (0.04 * x + 1.5);
    if ball_speed < starting_speed:
        ball_speed = starting_speed

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def game():
    global ball_speed, ball_x, ball_y, ball_movement
    global left_score, right_score

    # Set ball speed index
    x = 0.0

    # Set up the ball
    ball_x = window_width // 2 - ball_size // 2
    ball_y = window_height // 2 - ball_size // 2
    ball_movement = [1, -1]
    ball_speed = 1.0

    # Set up the score
    left_score = 0
    right_score = 0

    # Set us paddles
    left_paddle = pygame.Rect(0, window_height // 2 - pad_height // 2, pad_width, pad_height)
    right_paddle = pygame.Rect(window_width - pad_width, window_height // 2 - pad_height // 2, pad_width, pad_height)

    # Run the game loop
    running = True
    while running:
        # Process events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update the paddles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            running = False
        if keys[pygame.K_w]:
            left_paddle.y -= pad_speed
        if keys[pygame.K_s]:
            left_paddle.y += pad_speed
        if keys[pygame.K_UP]:
            right_paddle.y -= pad_speed
        if keys[pygame.K_DOWN]:
            right_paddle.y += pad_speed

        # Keep paddles on the screen
        if right_paddle.y < 0:
            right_paddle.y = 0
        if right_paddle.y + pad_height > window_height:
            right_paddle.y = window_height - pad_height
        if left_paddle.y < 0:
            left_paddle.y = 0
        if left_paddle.y + pad_height > window_height:
            left_paddle.y = window_height - pad_height

        # Update the ball
        ball_x += ball_movement[0] * ball_speed
        ball_y += ball_movement[1] * ball_speed

        # Keep ball on the screen
        if ball_y - ball_rad < 0:
            ball_y = ball_rad
            ball_movement[1] *= -1
        if ball_y + ball_rad > window_height:
            ball_y = window_height - ball_rad
            ball_movement[1] *= -1

        # Check if ball hits paddles
        if ball_x - ball_rad < left_paddle.right and ball_y > left_paddle.top and ball_y < left_paddle.bottom:
            ball_x = left_paddle.right + ball_rad
            ball_movement[0] *= -1
            x += 1
            speed(x)
        if ball_x + ball_rad > right_paddle.left and ball_y > right_paddle.top and ball_y < right_paddle.bottom:
            ball_x = right_paddle.left - ball_rad
            ball_movement[0] *= -1
            x += 1
            speed(x)

        # Check if ball hits goal edges
        if ball_x - ball_rad < 0:
            ball_x = ball_rad
            right_score += 1
            ball_movement[0] *= -1
            x -= 0.25
            speed(x)
            if left_score - 3 >= right_score or right_score - 3 > left_score:
                running = False
        if ball_x + ball_rad > window_width:
            left_score += 1
            ball_x = window_width - ball_rad
            ball_movement[0] *= -1
            x -= 0.25
            speed(x)
            if left_score - 3 >= right_score or right_score - 3 > left_score:
                running = False
        # Draw the game
        window.fill(BLACK)
        pygame.draw.rect(window, WHITE, left_paddle)
        pygame.draw.rect(window, WHITE, right_paddle)
        pygame.draw.circle(window, WHITE, (ball_x, ball_y), ball_size / 2)
        pygame.draw.rect(window, WHITE, pygame.Rect(window_width // 2 - 1, 0, 2, window_height))
        font = pygame.font.Font(None, 36)
        left = font.render("{}".format(left_score), True, WHITE)
        window.blit(left, (window_width / 2 - left.get_width() - 18, 18))
        right = font.render("{}".format(right_score), True, WHITE)
        window.blit(right, (window_width / 2 + 18, 18))
        pygame.display.flip()

    # Display winning screen
    font = pygame.font.Font(None, 36)
    message = None
    if left_score > right_score:
        message = font.render("Left side wins!", True, WHITE)
    else:
        message = font.render("Right side wins!", True, WHITE)
    window.fill(BLACK)
    window.blit(message, (window_width / 2 - message.get_width() / 2, window_height / 2 - message.get_height() / 2))
    font = pygame.font.Font(None, 24)
    message = font.render("Space to replay, Q to quit", True, WHITE)
    window.blit(message, (window_width / 2 - message.get_width() / 2, window_height / 2 + message.get_height()))
    pygame.display.flip()

    # Wait for user to either replay, or quit
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            running = False
        if keys[pygame.K_SPACE]:
            game()
            running = False

game()

pygame.quit()
