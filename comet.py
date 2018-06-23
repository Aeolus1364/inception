import random
import pygame
import cfg
import math


class Body(pygame.sprite.Sprite):
    def __init__(self, pos, mass, image):
        super(Body, self).__init__()

        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.centerx = pos[0]
        self.rect.centery = pos[1]

        self.mass = mass
        self.radius = self.rect.w / 2

        self.x_vel = 0
        self.y_vel = 0
        self.x_acc = 0
        self.y_acc = 0

    def apply_force(self, mag, ang):
        acc = mag / self.mass


body = Body((0, 0), 50, "meteor.png")
print(body.radius)


class Comet(pygame.sprite.Sprite):
    def __init__(self):
        super(Comet, self).__init__()

        self.image = pygame.image.load("meteor.png")
        self.image = pygame.transform.scale2x(pygame.image.load("meteor.png"))
        self.rect = self.image.get_rect()

        self.x_vel = 0
        self.y_vel = 0

        self.x_acc = 0
        self.y_acc = 0

        self.spawn()

    def spawn(self):
        vel = random.uniform(5, 8)
        # ang = random.randint(0, 360)

        side = random.choice(("up", "down", "left", "right"))

        if side == "up":
            length = random.randint(0, cfg.dim[0])
            self.rect.x = length
            self.rect.y = 0 - cfg.spawn_dist
            if length < cfg.dim[0] / 2:
                ang = random.randint(270, 270 + cfg.spawn_ang)
            else:
                ang = random.randint(270 - cfg.spawn_ang, 270)

        elif side == "down":
            length = random.randint(0, cfg.dim[0])
            self.rect.x = length
            self.rect.y = cfg.dim[1] + cfg.spawn_dist
            if length < cfg.dim[0] / 2:
                ang = random.randint(90 - cfg.spawn_ang, 90)
            else:
                ang = random.randint(90, 90 + cfg.spawn_ang)

        elif side == "left":
            length = random.randint(0, cfg.dim[1])
            self.rect.y = length
            self.rect.x = 0 - cfg.spawn_dist
            if length < cfg.dim[1] / 2:
                ang = random.randint(0, 0 + cfg.spawn_ang)
            else:
                ang = random.randint(0 - cfg.spawn_ang, 0)

        elif side == "right":
            length = random.randint(0, cfg.dim[1])
            self.rect.y = length
            self.rect.x = cfg.dim[0] + cfg.spawn_dist
            if length < cfg.dim[1] / 2:
                ang = random.randint(180, 180 + cfg.spawn_ang)
            else:
                ang = random.randint(180 - cfg.spawn_ang, 180)

        self.x_vel = vel * math.cos(math.radians(ang))
        self.y_vel = -vel * math.sin(math.radians(ang))

        print(self.rect.x, self.rect.y)
        print(ang)

    def update(self, *args):
        # print(self.x_acc, self.x_vel)
        self.x_vel += self.x_acc
        self.y_vel += self.y_acc
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        self.x_acc = 0
        self.y_acc = 0


class GroupComet(pygame.sprite.Group):
    def __init__(self):
        super(GroupComet, self). __init__()