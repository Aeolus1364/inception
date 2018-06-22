import pygame
import comet
import cfg


class Main:
    def __init__(self):
        pygame.init()

        self.running = True
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(cfg.dim)
        self.fps = 60

        self.comet = comet.Comet()
        # self.comet.spawn()
        self.group = comet.GroupComet()
        self.group.add(self.comet)

        print(self.surface.get_rect())


    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    if event.key == pygame.K_SPACE:
                        self.group.empty()

            # for i in self.group.sprites():
            #     # if not self.surface.get_rect().colliderect(i.rect):
            #     #     self.group.remove(i)
            #     cursor = pygame.mouse.get_pos()
            #     if i.rect.x > cursor[0]:
            #         i.x_vel -= 0.5
            #     else:
            #         i.x_vel += 0.5
            #
            #     if i.rect.y > cursor[1]:
            #         i.y_vel -= 0.5
            #     else:
            #         i.y_vel += 0.5

            self.surface.fill((0, 0, 0))

            self.group.update()

            self.group.draw(self.surface)

            if len(self.group.sprites()) < 100 :
                self.group.add(comet.Comet())

            # print(len(self.group.sprites()))

            pygame.display.update()
            self.clock.tick(self.fps)


main = Main()
main.main_loop()
