import pygame
from random import randint
import math


class Ball:
    def __init__(self, screen, first_ball):
        self.color = (255, 255, 0)
        self.radius = 7.5
        if first_ball:
            self.heading = randint(240, 300)
        else:
            self.heading = randint(60, 120)
        self.limits = (screen.get_width(), screen.get_height())
        self.position = pygame.Vector2(screen.get_width() / 2, (screen.get_height() / 2) + 90)
        self.speed = 400

    def move(self, dt):
        self.position.x += self.speed * math.cos(math.radians(self.heading)) * dt
        self.position.y -= self.speed * math.sin(math.radians(self.heading)) * dt

    def check_wall_bounce(self, screen):
        if self.position.x - 4 <= self.radius and 90 < self.heading < 270:
            self.heading = (540 - self.heading) % 360
        if self.position.x + 4 >= screen.get_width() - self.radius and (self.heading < 90 or self.heading > 270):
            self.heading = (540 - self.heading) % 360
        if self.position.y <= self.radius and 0 < self.heading < 180:
            self.heading = 360 - self.heading

    def check_paddle_bounce(self, paddle_pos, paddle_width, paddle_height):
        if (paddle_pos.y - paddle_height / 2) <= self.position.y + self.radius:
            if (paddle_pos.x - paddle_width / 2) < self.position.x < (paddle_pos.x + paddle_width / 2):
                self.heading = (((paddle_pos.x + paddle_width / 2) - self.position.x) / paddle_width) * 144 + 18

    def check_block_bounce(self, block):
        if block.position.y - 15 <= self.position.y <= block.position.y + 15:
            if block.position.x - 60 <= self.position.x + self.radius <= block.position.x and (self.heading < 90 or self.heading > 270):
                self.heading = (540 - self.heading) % 360
                return True
            elif block.position.x + 60 >= self.position.x - self.radius >= block.position.x and 90 < self.heading < 270:
                self.heading = (540 - self.heading) % 360
                return True
        if block.position.x - 60 <= self.position.x <= block.position.x + 60:
            if block.position.y + 15 >= self.position.y - self.radius >= block.position.y and self.heading < 180:
                self.heading = 360 - self.heading
                return True
            elif block.position.y - 15 <= self.position.y + self.radius <= block.position.y and self.heading > 180:
                self.heading = 360 - self.heading
                return True
        return False


class Paddle:
    def __init__(self, screen):
        self.height = 10
        self.width = 120
        self.color = (255, 255, 0)
        self.position = pygame.Vector2(screen.get_width() / 2, screen.get_height() - 30)
        self.speed = 300

    def not_reached_right_limit(self, screen):
        return self.position.x + self.width/2 <= screen.get_width()

    def not_reached_left_limit(self, screen):
        return self.position.x >= self.width/2

    def move_left(self, dt):
        self.position.x -= self.speed * dt

    def move_right(self, dt):
        self.position.x += self.speed * dt


class Block:
    def __init__(self, position, lives):
        self.width = 118
        self.height = 28
        self.position = pygame.Vector2(position[0], position[1])
        self.lives = lives
        self.r = 0
        self.g = 0
        self.b = 0
        if 0 < self.lives < 3:
            self.r = 155 + 50 * self.lives
            self.g = 0
            self.b = 0
        elif self.lives < 8:
            self.r = 255
            self.g = 0
            self.b = 55 + 50 * (self.lives - 3)
        elif self.lives < 13:
            self.r = 255
            self.g = 55 + 50 * (self.lives - 8)
            self.b = 255
        else:
            self.r = 255
            self.g = 255
            self.b = 255
        self.color = (self.r, self.g, self.b)

    def losing_life(self):
        self.lives -= 1
        if 0 < self.lives < 3:
            self.r = 155 + 50 * self.lives
            self.g = 0
            self.b = 0
        elif self.lives < 8:
            self.r = 255
            self.g = 0
            self.b = 55 + 50 * (self.lives - 3)
        elif self.lives < 13:
            self.r = 255
            self.g = 55 + 50 * (self.lives - 8)
            self.b = 255
        else:
            self.r = 255
            self.g = 255
            self.b = 255
        self.color = (self.r, self.g, self.b)

    @staticmethod
    def yield_surprise_pack():
        return randint(1, 3) == 2


class SurprisePack:
    def __init__(self, position):
        self.position = position
        self.speed = 300
        self.color = 'cyan'

    def move(self, dt):
        self.position[1] += self.speed * dt

    def surprise_pack_collected(self, paddle_position, paddle_width):
        if 700 < self.position[1] < 710 and paddle_position[0] - paddle_width/2 < self.position[0] < paddle_position[0] + paddle_width/2:
            return "caught"
        if 720 < self.position[1]:
            return "missed"

    @staticmethod
    def random_effect():
        effects = {1: "extra ball",
                   2: "longer paddle",
                   3: "shorter paddle",
                   4: "faster ball",
                   5: "faster paddle"}
        return effects[randint(1, 5)]