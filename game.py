import pygame
from gameelements import Ball, Paddle, Block
import json


def game(level):
    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((960, 720))
    clock = pygame.time.Clock()
    game_on = True
    dt = 0
    win = False

    # Creating instances
    paddle = Paddle(screen)
    ball = Ball(screen)
    blocks = []

    # Opening level
    with open(f"levels/level{level}.json") as level:
        data = json.load(level)
        for item in data:
            block = Block(item["position"], item["lives"])
            blocks.append(block)


    # Main loop
    while game_on:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # drawing graphic elements on the screen
        pygame.draw.rect(screen, paddle.color, pygame.Rect(paddle.position.x-paddle.width/2, paddle.position.y,
                                                           paddle.width, paddle.height), 5, 5)
        pygame.draw.circle(screen, ball.color, ball.position, ball.radius)

        for block in blocks:
            pygame.draw.rect(screen, block.color, pygame.Rect(block.position.x-block.width/2,
                                                              block.position.y-block.height/2, block.width, block.height))

        pygame.display.flip()

        # Controlling ball movement
        ball.move(dt)
        ball.check_wall_bounce(screen)
        ball.check_paddle_bounce(paddle.position, paddle.width, paddle.height)
        for block in blocks:
            if ball.check_block_bounce(block):
                block.losing_life()
                if block.lives == 0:
                    blocks.remove(block)
        pygame.display.flip()

        # Controlling paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.not_reached_left_limit(screen):
            paddle.move_left(dt)
        if keys[pygame.K_RIGHT] and paddle.not_reached_right_limit(screen):
            paddle.move_right(dt)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

        if ball.position.y > screen.get_height():
            game_on = False

        if not blocks:
            win = True
            game_on = False

    return win
