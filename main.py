import pygame
import body
import cfg
import calc
import button
import random


class Main:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)

        pygame.mixer.music.load("res/music.wav")
        pygame.mixer.music.play(-1)

        self.running = True
        self.pause = False
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(cfg.dim)
        self.fps = 60

        self.large_group = body.Group()
        self.medium_group = body.Group()
        self.small_group = body.Group()
        self.explode_group = body.Group()
        self.planet = body.Planet()
        self.mouse = body.Mouse()

        self.large_group.add(body.Large())

        for i in range(1):
            self.medium_group.add(body.Medium())

    def main_loop(self):
        grav_on = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    if event.key == pygame.K_SPACE:
                        self.medium_group.add(body.Medium())
                    if event.key == pygame.K_ESCAPE:
                        self.pause = True

                if event.type == pygame.MOUSEBUTTONDOWN:
                    grav_on = True
                    self.mouse.image = self.mouse.clicked
                if event.type == pygame.MOUSEBUTTONUP:
                    grav_on = False
                    self.mouse.image = self.mouse.unclicked

            if self.pause:
                self.menu_loop()
                self.pause = False

            if grav_on:
                calc.grav_iter(self.smalls(), self.mouse, True)
                calc.grav_iter(self.mediums(), self.mouse, True)
                calc.grav_iter(self.larges(), self.mouse, True)
            if self.planet.alive:
                calc.grav_iter(self.smalls(), self.planet)
                calc.grav_iter(self.mediums(), self.planet)
                calc.grav_iter(self.larges(), self.planet)

            self.small_group.update()
            self.medium_group.update()
            self.large_group.update()
            self.explode_group.update()

            self.mouse.update()

            self.surface.fill((0, 0, 0))

            self.small_group.draw(self.surface)
            self.medium_group.draw(self.surface)
            self.large_group.draw(self.surface)
            self.explode_group.draw(self.surface)
            self.planet.draw(self.surface)

            self.mouse.draw(self.surface)

            calc.clean_up(self.medium_group)
            calc.clean_up(self.small_group)

            for i in self.smalls():
                if calc.circ_coll(i, self.planet):
                    i.kill()
                    self.planet.mass += 0.5
                    self.planet.resize(1.01)

            for i in self.mediums():
                for j in self.mediums():
                    if not i == j:
                        if calc.circ_coll(i, j):
                            for k in range(random.randint(3, 8)):
                                self.small_group.add(body.Small(i.rect.center))
                            i.kill()
                            j.kill()
                if calc.circ_coll(i, self.planet):
                    if self.planet.alive:
                        i.kill()

            for i in self.mediums():
                for k in self.smalls():
                    if calc.circ_coll(i, k):
                        k.kill()

            for i in self.larges():
                for j in self.mediums():
                    if calc.circ_coll(i, j):
                        for k in range(random.randint(3, 8)):
                            self.small_group.add(body.Small(i.rect.center))
                            j.kill()
                if calc.circ_coll(i, self.planet):
                    i.kill()
                    for k in range(random.randint(5, 10)):
                        self.explode_group.add(body.Medium(self.planet.rect.center))
                    for k in range(random.randint(30, 40)):
                        self.explode_group.add(body.Small(self.planet.rect.center))
                    self.planet.kill()
                    self.fps = 10

            if len(self.medium_group.sprites()) < 5:
                self.medium_group.add(body.Medium())

            pygame.display.update()
            self.clock.tick(self.fps)

    def menu_loop(self):
        group = pygame.sprite.Group()
        group.add(button.Button(self.surface.get_rect().center, "Test"))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse.image = self.mouse.clicked
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouse.image = self.mouse.unclicked

            self.mouse.update()

            self.surface.fill((0, 0, 0))

            self.small_group.draw(self.surface)
            self.medium_group.draw(self.surface)
            self.large_group.draw(self.surface)
            self.planet.draw(self.surface)

            group.draw(self.surface)

            self.mouse.draw(self.surface)

            pygame.display.update()
            self.clock.tick(self.fps)

    def larges(self):
        return self.large_group.sprites()

    def mediums(self):
        return self.medium_group.sprites()

    def smalls(self):
        return self.small_group.sprites()


main = Main()
main.main_loop()
