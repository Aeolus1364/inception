import random
import pygame
import cfg
import math
import calc
import res


class Body(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()

        self.radius = self.rect.w / 2
        self.mass = 0

        self.x_vel = 0
        self.y_vel = 0
        self.x_acc = 0
        self.y_acc = 0

        self.x = 0
        self.y = 0

    def transpose(self):
        self.rect.x = round(self.x)
        self.rect.y = round(self.y)

    def update(self, *args):
        self.x_vel += self.x_acc
        self.y_vel += self.y_acc
        self.x += self.x_vel
        self.y += self.y_vel

        self.x_acc = 0
        self.y_acc = 0

        self.transpose()


class Object(Body):
    def __init__(self, image, spawn_loc=None):
        super().__init__(image)
        factor = random.uniform(0.8, 1.25)
        self.rect, self.image = calc.resize(self.rect, self.image, factor)
        self.radius = self.rect.w / 2

        if spawn_loc:
            self.spawn_collision(1, 4, spawn_loc)
        else:
            self.spawn_offscreen(2, 4)

    def spawn_offscreen(self, vmin, vmax):
        vel = random.uniform(vmin, vmax)
        ang = 0

        side = random.choice(("up", "down", "left", "right"))

        if side == "up":
            length = random.randint(0, cfg.dim[0])
            self.x = length
            self.y = 0 - cfg.spawn_dist
            if length < cfg.dim[0] / 2:
                ang = random.randint(270, 270 + cfg.spawn_ang)
            else:
                ang = random.randint(270 - cfg.spawn_ang, 270)

        elif side == "down":
            length = random.randint(0, cfg.dim[0])
            self.x = length
            self.y = cfg.dim[1] + cfg.spawn_dist
            if length < cfg.dim[0] / 2:
                ang = random.randint(90 - cfg.spawn_ang, 90)
            else:
                ang = random.randint(90, 90 + cfg.spawn_ang)

        elif side == "left":
            length = random.randint(0, cfg.dim[1])
            self.y = length
            self.x = 0 - cfg.spawn_dist
            if length < cfg.dim[1] / 2:
                ang = random.randint(0, 0 + cfg.spawn_ang)
            else:
                ang = random.randint(0 - cfg.spawn_ang, 0)

        elif side == "right":
            length = random.randint(0, cfg.dim[1])
            self.y = length
            self.x = cfg.dim[0] + cfg.spawn_dist
            if length < cfg.dim[1] / 2:
                ang = random.randint(180, 180 + cfg.spawn_ang)
            else:
                ang = random.randint(180 - cfg.spawn_ang, 180)

        self.x_vel = int(vel * math.cos(math.radians(ang)))
        self.y_vel = int(-vel * math.sin(math.radians(ang)))

    def spawn_collision(self, vmin, vmax, center):
        self.rect.center = center
        self.x, self.y = self.rect.topleft
        num = random.uniform(vmin, vmax)
        self.x_vel, self.y_vel = calc.vect2grid(num, random.randint(0, 360))


class Small(Object):
    def __init__(self, spawn_loc=None):
        super().__init__(res.meteoroid, spawn_loc)


class Medium(Object):
    def __init__(self, spawn_loc=None):
        super().__init__(res.asteroid, spawn_loc)
        self.mass = 25


class Large(Object):
    def __init__(self, spawn_loc=None):
        super().__init__(res.planetoid, spawn_loc)


class Group(pygame.sprite.Group):
    def __init__(self):
        super(). __init__()


class Planet(Body):
    def __init__(self):
        super().__init__(res.asteroid)
        self.image_original = self.image
        self.rect_original = self.rect

        self.alive = True
        self.rect.center = (cfg.dim[0] / 2, cfg.dim[1] / 2)
        # self.x, self.y = self.rect.topleft
        self.mass = 15
        self.size = 1
        #
        # print(self.x, self.y)
        # print(self.rect.topleft)

    def draw(self, surf):
        if self.alive:
            surf.blit(self.image, self.rect)
        if self.radius > 48:
            self.image_original = res.roundy
        if self.radius > 80:
            self.image_original = res.planetoid
        if self.radius > 128:
            self.image_original = res.planet
        if self.radius > 200:
            self.image_original = res.gasgiant
        if self.radius > 260:
            self.image_original = res.star

    def kill(self):
        self.alive = False

    def bombard(self):
        if self.mass < 20:
            self.kill()
            return False
        elif self.mass < 150:
            self.mass -= 2
            return True
        else:
            self.mass += 4
        return self.alive

    def resize(self, factor):
        self.size *= factor

        self.rect, self.image = calc.resize(self.rect_original, self.image_original, self.size)

        self.radius = self.rect.w / 2

    def update_loc(self):
        self.rect.center = (cfg.dim[0] / 2, cfg.dim[1] / 2)


class Mouse(Body):
    def __init__(self):
        super().__init__(res.mouse_clicked)
        self.mass = 100
        self.clicked = res.mouse_clicked
        self.unclicked = res.mouse_unclicked
        self.image = self.unclicked
        self.state = False

    def update(self, *args):
        self.rect.center = pygame.mouse.get_pos()
        self.state = pygame.mouse.get_pressed()[0]

        if self.state:
            self.image = self.clicked
        else:
            self.image = self.unclicked

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def pos(self):
        return self.rect.center

