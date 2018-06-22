import pygame
import comet


class Main:
    def __init__(self):
        pygame.init()

        self.running = True
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode((600, 400), pygame.RESIZABLE)
        self.fps = 30

        self.pixel = comet.Comet()
        self.group = pygame.sprite.Group(self.pixel)

    def main_loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.surface.fill((0, 0, 0))
            self.group.draw(self.surface)
            pygame.display.update()
            self.clock.tick(self.fps)


main = Main()
main.main_loop()
