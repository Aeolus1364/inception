import random
import pygame
import cfg
import math
import calc
import res


class Body(pygame.sprite.Sprite):
    def __init__(self, mass):
        super().__init__()
        self.mass = mass

        self.x_vel = 0
        self.y_vel = 0
        self.x_acc = 0
        self.y_acc = 0
        self.x = 0
        self.y = 0

        self.radius = 0
        self.image = None
        self.rect = None

        self.circle()

    def add(self, mass):
        self.mass += mass
        center = self.rect.center
        self.circle()
        self.rect.center = center

    def circle(self):
        self.radius = int(math.sqrt(self.mass / math.pi))
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, (255, 255, 255), self.rect.center, self.radius)

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
    def __init__(self, mass, spawn_loc=None):
        self.mass = mass
        super().__init__(self.mass)

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
        num = 0
        self.x_vel, self.y_vel = calc.vect2grid(num, random.randint(0, 360))


class Group(pygame.sprite.Group):
    def __init__(self):
        super(). __init__()


class Planet(Body):
    def __init__(self):
        super().__init__(3200)
        self.alive = True
        self.rect.center = (cfg.dim[0] / 2, cfg.dim[1] / 2)
        self.draw_text()

    def draw(self, surf):
        if self.alive:
            surf.blit(self.image, self.rect)

    def add(self, mass):
        super().add(mass)
        self.draw_text()

    def draw_text(self):
        font = pygame.font.SysFont("Arial", int(self.radius / 2))
        render = font.render(str(self.mass), True, (0, 0, 0))
        fontrect = render.get_rect()
        fontrect.center = self.image.get_rect().center

        self.image.blit(render, fontrect)

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

    def update_loc(self):
        self.rect.center = (cfg.dim[0] / 2, cfg.dim[1] / 2)


class Mouse():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.mass = 1000
        self.clicked = res.mouse_clicked
        self.unclicked = res.mouse_unclicked
        self.image = self.unclicked
        self.rect = self.image.get_rect()
        self.radius = self.rect.w / 2
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

