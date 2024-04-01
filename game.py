import pygame
from gameelements import Ball, Paddle, Block, SurprisePack
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
    initial_ball = Ball(screen, True)
    balls = [initial_ball]
    blocks = []
    surprise_packs = []

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

        # Blocks graphics
        for block in blocks:
            pygame.draw.rect(screen, block.color, pygame.Rect(block.position.x-block.width/2,
                                                              block.position.y-block.height/2, block.width, block.height))
        # Paddle graphics and logic
        pygame.draw.rect(screen, paddle.color, pygame.Rect(paddle.position.x-paddle.width/2, paddle.position.y,
                                                           paddle.width, paddle.height), 5, 5)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.not_reached_left_limit(screen):
            paddle.move_left(dt)
        if keys[pygame.K_RIGHT] and paddle.not_reached_right_limit(screen):
            paddle.move_right(dt)

        # Balls graphics and logic
        for ball in balls:
            pygame.draw.circle(screen, ball.color, ball.position, ball.radius)

            ball.move(dt)
            ball.check_wall_bounce(screen)
            ball.check_paddle_bounce(paddle.position, paddle.width, paddle.height)
            if ball.position.y > screen.get_height():
                balls.remove(ball)
            for block in blocks:
                if ball.check_block_bounce(block):
                    block.losing_life()
                    if block.lives == 0:
                        blocks.remove(block)
                        if block.yield_surprise_pack():
                            new_surprise_pack = SurprisePack(block.position)
                            surprise_packs.append(new_surprise_pack)

        # surprise packs graphics and logic
            for surprise_pack in surprise_packs:
                pygame.draw.rect(screen, surprise_pack.color, pygame.Rect(surprise_pack.position.x - 15,
                                                                          surprise_pack.position.y - 15, 15, 15))
                surprise_pack.move(dt)
                if surprise_pack.surprise_pack_collected(paddle.position, paddle.width) == "caught":
                    effect = surprise_pack.random_effect()
                    if effect == "extra ball":
                        extra_ball = Ball(screen, False)
                        balls.append(extra_ball)
                    if effect == "longer paddle":
                        paddle.width *= 1.5
                    if effect == "shorter paddle":
                        paddle.width *= 0.75
                    if effect == "faster ball":
                        ball.speed += 100
                    if effect == "faster paddle":
                        paddle.speed += 100
                    surprise_packs.remove(surprise_pack)

                if surprise_pack.surprise_pack_collected(paddle.position, paddle.width) == "missed":
                    surprise_packs.remove(surprise_pack)



        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

        if not balls:
            game_on = False

        if not blocks:
            win = True
            game_on = False

    return win
