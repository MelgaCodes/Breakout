import pygame


class Arrow:
    def __init__(self, screen):
        self.screen = screen
        self.color = 'white'
        self.points = [(610, 360), (630, 376), (630, 366), (670, 366), (670, 354), (630, 354), (630, 344)]

    def render_graphics(self):
        pygame.draw.polygon(self.screen, self.color, self.points)

    def game_start_animation(self):
        self.color = 'cyan'
        self.render_graphics()
        pygame.display.flip()
        pygame.time.wait(250)
        self.color = 'white'
        self.render_graphics()
        pygame.display.flip()
        pygame.time.wait(250)
        self.color = 'cyan'
        self.render_graphics()
        pygame.display.flip()
        pygame.time.wait(250)
        self.color = 'white'
        self.render_graphics()
        pygame.display.flip()
        pygame.time.wait(250)