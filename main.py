import pygame
import body
import cfg
import calc
import math
import random


class Main:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(False)

        self.running = True
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(cfg.dim)
        self.fps = 60

        self.comet_group = body.GroupComet()
        self.matter_group = body.GroupComet()
        self.planet = body.Planet()
        self.mouse = body.Mouse()

        for i in range(8):
            self.comet_group.add(body.Comet())

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
                        self.comet_group.add(body.Comet())


                if event.type == pygame.MOUSEBUTTONDOWN:
                    grav_on = True
                    self.mouse.image = self.mouse.clicked
                if event.type == pygame.MOUSEBUTTONUP:
                    grav_on = False
                    self.mouse.image = self.mouse.unclicked


            if grav_on:
                calc.grav_iter(self.comet_group.sprites(), self.mouse, True)
                calc.grav_iter(self.matter_group.sprites(), self.mouse, True)

            # print(self.planet.mass)

            calc.grav_iter(self.matter_group.sprites(), self.planet)
            calc.grav_iter(self.comet_group.sprites(), self.planet)

            self.surface.fill((0, 0, 0))

            self.comet_group.update()
            self.matter_group.update()
            self.mouse.update()

            self.matter_group.draw(self.surface)
            self.comet_group.draw(self.surface)
            self.planet.draw(self.surface)
            self.mouse.draw(self.surface)

            calc.clean_up(self.comet_group)
            calc.clean_up(self.matter_group)

            sprites = self.comet_group.sprites()

            for i in self.matter_group.sprites():
                if calc.circ_coll(i, self.planet):
                    i.kill()
                    self.planet.mass += 0.5
                    self.planet.resize(1.01)

            for i in self.comet_group.sprites():
                if calc.circ_coll(i, self.planet):
                    i.kill()

            for i in sprites:
                for j in sprites:
                    if not i == j:
                        if calc.circ_coll(i, j):
                            for k in range(random.randint(3, 8)):
                                self.matter_group.add(body.Matter(i.rect.center))
                            i.kill()
                            j.kill()

            # print(len(self.matter_group.sprites()) + len(self.comet_group))
            print(self.planet.size)

            if len(self.comet_group.sprites()) < 2:
                self.comet_group.add(body.Comet())

            pygame.display.update()
            # print(self.clock.get_fps())
            self.clock.tick(self.fps)


main = Main()
main.main_loop()
