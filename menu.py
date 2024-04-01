import pygame
import os
import game
from menuelements import Arrow
import levelbuilder


# pygame setup
pygame.init()
pygame.font.init()
menu_screen = pygame.display.set_mode((960, 720))
clock = pygame.time.Clock()
menu_font = pygame.font.SysFont("", 45)
running = True
position = 0
arrow = Arrow(menu_screen)
available_levels = {1}
saved_levels = {0}
all_levels = set([level for level in range(0, len(os.listdir()))])
test_mode = False

while running:
    level_list = os.listdir("levels")
    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and position + 1 in available_levels:
                arrow.game_start_animation()
                won = game.game(position + 1)
                menu_screen.fill("black")
                if won:
                    available_levels.add(position + 2)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and position < len(level_list) - 1:
                position += 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN and position > 0:
                position -= 1
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_l:
                levelbuilder.level_builder()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t and not test_mode:
                saved_levels = available_levels
                available_levels = all_levels
                test_mode = True
            elif event.key == pygame.K_t and test_mode:
                available_levels = saved_levels
                test_mode = False
        # pygame.QUIT event means the user clicked X to close your window
        if event.type == pygame.QUIT:
            running = False

    # Rendering graphics
    menu_screen.fill("black")
    arrow.render_graphics()
    y_first_button = menu_screen.get_height() / 2 - 30 + position * 75
    pygame.draw.rect(menu_screen, (255, 255, 0), pygame.Rect(menu_screen.get_width()/2 - 120,
                                                             y_first_button, 240, 60),
                     5, 5)
    text_surface = menu_font.render("LEVEL 1", False, (255, 255, 255))
    menu_screen.blit(text_surface, (menu_screen.get_width()/2 - 57, y_first_button + 16))
    for i in range(0, len(level_list) - 1):
        if i + 2 in available_levels:
            pygame.draw.rect(menu_screen, (255, 255, 0), pygame.Rect(menu_screen.get_width()/2 - 120, y_first_button - 75 * (i+1), 240, 60),
                             5, 5)
            text_surface = menu_font.render(f"LEVEL {i + 2}", False, (255, 255, 255))
            menu_screen.blit(text_surface, (menu_screen.get_width() / 2 - 57, y_first_button - 75 * (i + 1) + 16))
        else:
            pygame.draw.rect(menu_screen, (200, 0, 0),
                             pygame.Rect(menu_screen.get_width() / 2 - 120, y_first_button - 75 * (i + 1), 240, 60),
                             5, 5)
            text_surface = menu_font.render(f"LEVEL {i + 2}", False, (200, 0, 0))
            menu_screen.blit(text_surface, (menu_screen.get_width() / 2 - 57, y_first_button - 75 * (i + 1) + 16))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()
