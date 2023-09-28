import pygame


class Bird:
    def __init__(
        self, position, max_speed, max_force, radius, color, screen_width, screen_height
    ):
        self.position = position
        self.max_speed = max_speed
        self.max_force = max_force
        self.radius = radius
        self.color = color
        self.mass = 1
        self.velocity = pygame.math.Vector2(0, 0)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.acceleration = pygame.math.Vector2(0, 0)

    def seek(self, target):
        desired = target - self.position
        desired = desired.normalize()
        desired *= self.max_speed
        steer = desired - self.velocity
        return steer

    def update(self, dt, mouse_pos, birds):
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
        if self.position.x < 0 or self.position.x > self.screen_width:
            self.velocity.x *= -1
        if self.position.y < 0 or self.position.y > self.screen_height:
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
