import pygame
import random


refresh_rate = 60
screen_width = 800
screen_height = 600

trails_enabled = True

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True
dt = 0
birds = []
current_mouse_position = pygame.mouse.get_pos()
bird_count = random.randint(50, 200)
speed_multiplier = 3
trail_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
prev_bird_positions = []
max_prev_positions = 1000

class Bird:
    position = pygame.math.Vector2(0, 0)
    velocity = pygame.math.Vector2(0, 0)
    acceleration = pygame.math.Vector2(0, 0)
    max_speed = random.randint(10, 100)
    max_force = random.randint(10, 100)
    radius = random.randint(1, 3)
    color = (255, 255, 255)
    mass = 1

    def __init__(self, position, max_speed, max_force, radius, color):
        self.position = position
        self.max_speed = max_speed
        self.max_force = max_force
        self.radius = radius
        self.color = color
        self.mass = 1
        self.velocity = pygame.math.Vector2(0, 0)

    def seek(self, target):
        desired = target - self.position
        desired = desired.normalize()
        desired *= self.max_speed
        steer = desired - self.velocity
        return steer
    
    def update(self, dt, mouse_pos):
        # Seek the mouse position
        steer = self.seek(mouse_pos)
        self.acceleration += steer / self.mass

        # Update the velocity and position of the bird
        self.velocity += self.acceleration * dt
        if self.velocity.length() > 0:
            self.velocity.scale_to_length(min(self.velocity.length(), self.max_speed))
        else:
            self.velocity = pygame.math.Vector2(0.1, 0)
        self.position += self.velocity * dt
        self.acceleration *= 0

        # Reflect bird off the screen edges
        if self.position.x < 0 or self.position.x > screen_width:
            self.velocity.x *= -1
        if self.position.y < 0 or self.position.y > screen_height:
            self.velocity.y *= -1

        for bird in birds:
            if bird != self:
                if (
                    pygame.math.Vector2.distance_to(self.position, bird.position)
                    < self.radius + bird.radius
                ):
                    # Calculate the normal vector pointing away from the collision
                    normal = pygame.math.Vector2.normalize(
                        self.position - bird.position
                    )

                    # Calculate the relative velocity of the birds
                    relative_velocity = self.velocity - bird.velocity

                    # Calculate the impulse magnitude
                    impulse_magnitude = (
                        -2
                        * pygame.math.Vector2.dot(relative_velocity, normal)
                        / (1 / self.mass + 1 / bird.mass)
                    ) * 1.25

                    # Calculate the impulse vector
                    impulse = impulse_magnitude * normal

                    # Update the velocities of the birds using the impulse
                    self.velocity += impulse / self.mass
                    bird.velocity -= impulse / bird.mass

                    # Move the birds slightly apart to avoid overlap
                    overlap = (
                        self.radius
                        + bird.radius
                        - pygame.math.Vector2.distance_to(self.position, bird.position)
                    )
                    self.position += overlap / 2 * normal
                    bird.position -= overlap / 2 * normal

        # Update the position of the current bird
        self.position += self.velocity * dt


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
            )
        )


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Clear the screen

    current_mouse_position = pygame.mouse.get_pos()

    #draw a red cursor at the mouse position
    pygame.draw.rect(screen, (255, 0, 0), (current_mouse_position[0] - 5, current_mouse_position[1] - 5, 10, 10))

    for bird in birds:
        bird.update(dt, current_mouse_position)
        pygame.draw.circle(
            screen,
            bird.color,
            (int(bird.position.x), int(bird.position.y)),
            bird.radius,
        )

        # Add the current bird position to the list
        prev_bird_positions.append((bird.position.copy(), bird.radius))  # Store both position and radius

        # Keep only the last 'max_prev_positions' positions to limit the trail length
        if len(prev_bird_positions) > max_prev_positions:
            prev_bird_positions.pop(0)

    # Clear the trail surface
    trail_surface.fill((0, 0, 0, 0))

    if trails_enabled:
        # Draw the trails using the previous bird positions and radius
        for pos, radius in prev_bird_positions:
            pygame.draw.circle(
                trail_surface,
                (255, 255, 255, 10),  # Trail color with transparency
                (int(pos.x), int(pos.y)),
                radius,  # Use the bird's radius as the trail width
            )

        # Set the alpha value of the trail surface to 128
        trail_surface.set_alpha(128)

        # Draw the trail surface on the screen with alpha blending
        screen.blit(trail_surface, (1, 0), special_flags=pygame.BLEND_RGBA_ADD)

    pygame.display.flip()
    dt = clock.tick(refresh_rate) / 1000

pygame.quit()
