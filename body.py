import random
import pygame
import cfg
import math
import calc


class Body(pygame.sprite.Sprite):
    def __init__(self, image=""):
        super(Body, self).__init__()

        if image:
            self.image = pygame.image.load(image)
            self.image = pygame.transform.scale2x(self.image)
        else:
            self.image = pygame.Surface((0, 0))

        self.rect = self.image.get_rect()
        self.radius = self.rect.w / 2
        self.mass = 0

        self.x_vel = 0
        self.y_vel = 0
        self.x_acc = 0
        self.y_acc = 0

    def update(self, *args):
        self.x_vel += self.x_acc
        self.y_vel += self.y_acc
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

        self.x_acc = 0
        self.y_acc = 0


class Comet(Body):
    def __init__(self):
        super(Comet, self).__init__("meteor.png")

        self.mass = 25
        self.spawn()

    def spawn(self):
        vel = random.uniform(3, 5)
        ang = 0

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

        # print(self.rect.x, self.rect.y)
        # print(ang)


class GroupComet(pygame.sprite.Group):
    def __init__(self):
        super(GroupComet, self). __init__()


class Matter(Body):
    def __init__(self, center):
        super(Matter, self).__init__("matter.png")

        self.rect.center = center

        self.x_vel, self.y_vel = calc.vect2grid(random.uniform(1, 5), random.randint(0, 360))


class Planet(Body):
    def __init__(self):
        super(Planet, self).__init__("planet.png")

        self.image_original = self.image
        self.rect_original = self.rect

        self.alive = True
        self.rect.center = (cfg.dim[0] / 2, cfg.dim[1] / 2)
        self.mass = 10
        self.size = 1

    def draw(self, surf):
        if self.alive:
            surf.blit(self.image, self.rect)

    def kill(self):
        self.alive = False

    def bombard(self, mass):
        ratio = mass/self.mass
        if ratio < cfg.min_ratio:
            return False
        elif ratio > cfg.max_ratio:
            return True
        else:
            prob = ratio / cfg.mult_ratio
            return random.choices((True, False), (prob, 1))

    def resize(self, factor):
        self.size *= factor

        # center = self.rect.center
        # size = int(self.rect_original.w * self.size), int(self.rect_original.h * self.size)
        # self.image = pygame.transform.scale(self.image_original, size)
        # self.rect = self.image.get_rect()
        # self.rect.center = center

        self.rect, self.image = calc.resize(self.rect_original, self.image_original, self.size)

        self.radius = self.rect.w / 2


class Mouse(Body):
    def __init__(self):
        super(Mouse, self).__init__("mouse1.png")
        self.mass = 100
        self.clicked = pygame.image.load("mouse2.png")
        self.clicked = pygame.transform.scale2x(self.clicked)
        self.unclicked = pygame.image.load("mouse1.png")
        self.unclicked = pygame.transform.scale2x(self.unclicked)

    def update(self, *args):
        self.rect.center = pygame.mouse.get_pos()

    def draw(self, surf):
        surf.blit(self.image, self.rect)
