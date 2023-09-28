import pygame
import random
from bird import Bird

# Configuration Constants
refresh_rate = 60
screen_width = 800
screen_height = 600
trails_enabled = True
speed_multiplier = 3
max_prev_positions = 1000

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0
birds = []
current_mouse_position = pygame.mouse.get_pos()
bird_count = random.randint(50, 200)
trail_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
prev_bird_positions = []

if birds == []:
    for i in range(0, bird_count):
        birds.append(
            Bird(
                pygame.math.Vector2(
                    random.randint(0, screen_width),
                    random.randint(0, screen_height),
                ),
                random.randint(10, 100 * speed_multiplier),
                random.randint(10, 100 * speed_multiplier),
                random.randint(1, 3),
                (255, 255, 255),
                screen_width,
                screen_height,
            )
        )
