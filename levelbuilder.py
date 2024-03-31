import pygame
from pygame.locals import *
import os


def level_builder():
    # Returns a rgb color depending on the number of lives of the block
    def block_color(lives):
        if 0 < lives < 3:
            r = 155 + 50 * lives
            g = 0
            b = 0
        elif lives < 8:
            r = 255
            g = 0
            b = 55 + 50 * (lives - 3)
        elif lives < 12:
            r = 255
            g = 55 + 50 * (lives - 8)
            b = 255
        else:
            r = 255
            g = 255
            b = 255
        color = (r, g, b)
        return color

    # pygame setup
    pygame.init()
    builder_screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()
    level_builder_on = True

    block_list = []
    block_list_positions = []

    while level_builder_on:
        # Event's poll
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level_builder_on = False
            # Adds a life to a block when left-clicking on it. Creates a new block if the allotment is empty
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                block_list_positions = [block['position'] for block in block_list]
                x = pygame.mouse.get_pos()[0] - (pygame.mouse.get_pos()[0] % 120)
                y = pygame.mouse.get_pos()[1] - (pygame.mouse.get_pos()[1] % 30)
                new_block = {"position": [x, y], "lives": 1}
                block_not_in_list = True
                if [x, y] not in block_list_positions:
                    block_list.append(new_block)
                else:
                    for block in block_list:
                        if block["position"] == [x, y] and block["lives"] < 12:
                            block["lives"] += 1
            # Takes a life from a block when right-clicking on it. If it was the block's last life, it destroys it
            if event.type == MOUSEBUTTONDOWN and event.button == 3:
                x = pygame.mouse.get_pos()[0] - (pygame.mouse.get_pos()[0] % 120)
                y = pygame.mouse.get_pos()[1] - (pygame.mouse.get_pos()[1] % 30)
                if not block_list:
                    continue
                for block in block_list:
                    if block["position"] == [x, y] and block["lives"] > 0:
                        block["lives"] -= 1
                        if block["lives"] == 0:
                            block_list.remove(block)
                        break
            # When pressing the spacebar, creates a JSON file with the positions and number of lives of the blocks visible on the screen
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                for block in block_list:
                    block["position"][0] += 60
                    block["position"][1] += 15
                level_number = len(os.listdir("levels")) + 1
                level_name = f"level{level_number}"
                with open(f"levels/{level_name}.json", "w") as file:
                    file.write(str(block_list).replace("'", '"'))
                level_builder_on = False
                break

            # Graphics rendering
        builder_screen.fill("black")
        horizontal_pos_grid = 119
        vertical_pos_grid = 29
        for _ in range(0, 7):
            pygame.draw.rect(builder_screen, 'gray', (horizontal_pos_grid, 0, 2, builder_screen.get_height()))
            horizontal_pos_grid += 120
        for _ in range(0, 23):
            pygame.draw.rect(builder_screen, 'gray', (0, vertical_pos_grid, builder_screen.get_width(), 2))
            vertical_pos_grid += 30

        for block in block_list:
            pygame.draw.rect(builder_screen, block_color(block["lives"]), (block["position"][0], block["position"][1], 118, 28))

        pygame.display.flip()