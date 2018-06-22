import pygame


class Comet(pygame.sprite.Sprite):
    def __init__(self):
        super(Comet, self).__init__()

        self.rect = pygame.Rect(50, 50, 16, 16)
        self.image = pygame.image.load("circle.png")

        self.image = pygame.transform.scale(self.image, (16, 16))

        self.x_vel = 0
        self.y_vel = 0

    def spawn