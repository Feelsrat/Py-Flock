import pygame
from config import (
    refresh_rate,
    screen,
    clock,
    running,
    dt,
    current_mouse_position,
    birds,
    trail_surface,
    prev_bird_positions,
    max_prev_positions,
    trails_enabled,
)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # Clear the screen

    current_mouse_position = pygame.mouse.get_pos()

    # draw a red cursor at the mouse position
    pygame.draw.rect(
        screen,
        (255, 0, 0),
        (current_mouse_position[0] - 5, current_mouse_position[1] - 5, 10, 10),
    )

    for bird in birds:
        bird.update(dt, current_mouse_position, birds)
        pygame.draw.circle(
            screen,
            bird.color,
            (int(bird.position.x), int(bird.position.y)),
            bird.radius,
        )

        # Add the current bird position to the list
        prev_bird_positions.append(
            (bird.position.copy(), bird.radius)
        )  # Store both position and radius

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
