import pygame
import comet
import cfg
import calc
import math


class Main:
    def __init__(self):
        pygame.init()

        self.running = True
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(cfg.dim, pygame.FULLSCREEN)
        self.fps = 60

        self.comet = comet.Comet()
        # self.comet.spawn()
        self.group = comet.GroupComet()
        self.group.add(self.comet)

        print(self.surface.get_rect())

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
                        self.group.add(comet.Comet())
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        grav_on = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    grav_on = True
                if event.type == pygame.MOUSEBUTTONUP:
                    grav_on = False


            if grav_on:
                for i in self.group.sprites():
                    i.x_acc, i.y_acc = calc.grav_acc((i.rect.centerx, i.rect.centery), (pygame.mouse.get_pos()), 50)

            self.surface.fill((0, 0, 0))

            self.group.update()

            self.group.draw(self.surface)

            # for i in self.group.sprites():
            #     for j in self.group.sprites():
            #         if calc.circ_coll(i.rect.center, 32, j.rect.center, 32):
            #             if not i == j:
            #                 print("SMASH")
            #                 i.kill()
            #                 j.kill()

            sprites = self.group.sprites()

            for i in sprites:
                sprites.remove(i)
                for j in sprites:
                    if calc.circ_coll(i.rect.center, 32, j.rect.center, 32):
                        print("SMASH")
                        i.kill()
                        j.kill()

            if len(self.group.sprites()) < 4:
                self.group.add(comet.Comet())

            # print(len(self.group.sprites()))

            pygame.display.update()
            # print(pygame.time.get_ticks())
            self.clock.tick(self.fps)


main = Main()
main.main_loop()
