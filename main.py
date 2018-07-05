import pygame
import body
import cfg
import calc
import random
import time
import res
import menu

pygame.init()
pygame.mixer.music.load("res/music.wav")
pygame.mixer.music.play(-1)


class Main:
    def __init__(self):
        pygame.mouse.set_visible(False)

        pygame.display.set_caption("Inception")
        pygame.display.set_icon(res.asteroid)

        self.running = True
        self.restart = False
        self.fullscreen = cfg.fullscreen
        self.clock = pygame.time.Clock()
        if self.fullscreen:
            self.surface = pygame.display.set_mode(cfg.dim, pygame.FULLSCREEN)
        else:
            self.surface = pygame.display.set_mode(cfg.dim, pygame.RESIZABLE)

        self.fps = 30

        self.time_init = time.time()
        self.wait = 0

        self.large_group = body.Group()
        self.medium_group = body.Group()
        self.small_group = body.Group()
        self.explode_group = body.Group()
        self.planet = body.Planet()
        self.mouse = body.Mouse()

        button1 = menu.Button("Resume", 30, (cfg.dim[0] / 2, 250))
        button2 = menu.Button("Restart", 30, (cfg.dim[0] / 2, 325))

        self.buttons = [
            menu.Button("Resume", 30, (cfg.dim[0] / 2, 250)),
            menu.Button("Restart", 30, (cfg.dim[0] / 2, 325)),
            menu.Button("Controls", 30, (cfg.dim[0] / 2, 400)),
            menu.Button("Main Menu", 30, (cfg.dim[0] / 2, 475))
        ]

        self.buttons = [button1, button2]

        self.menu = menu.Menu(self.buttons)

        self.main_loop()

    def main_loop(self):
        grav_on = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    if event.key == pygame.K_ESCAPE:
                        if self.planet.alive:
                            self.menu_loop()
                    if event.key == pygame.K_f:
                        if self.fullscreen:
                            self.surface = pygame.display.set_mode((self.sd.current_w, self.sd.current_h), pygame.FULLSCREEN)
                            self.fullscreen = False
                        else:
                            self.surface = pygame.display.set_mode(cfg.dim)
                            self.fullscreen = True
                    if event.key == pygame.K_r:
                        self.running = False
                        self.restart = True

            if self.mouse.state:
                grav_on = True
            else:
                grav_on = False

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

            self.spawn()

            self.sd = pygame.display.Info()

            calc.clean_up(self.explode_group)
            calc.clean_up(self.large_group)
            calc.clean_up(self.medium_group)
            calc.clean_up(self.small_group)

            for i in self.smalls():
                if calc.circ_coll(i, self.planet):
                    i.kill()
                    self.planet.mass += 0.5
                    self.planet.resize(1.02)

            for i in self.mediums():
                for j in self.mediums():
                    if not i == j:
                        if calc.circ_coll(i, j):
                            for k in range(random.randint(5, 10)):
                                self.small_group.add(body.Small(i.rect.center))
                            i.kill()
                            j.kill()
                if calc.circ_coll(i, self.planet):
                    if self.planet.alive:
                        response = self.planet.bombard()
                        if not response:
                            for k in range(random.randint(5, 10)):
                                self.explode_group.add(body.Medium(self.planet.rect.center))
                            for k in range(random.randint(30, 40)):
                                self.explode_group.add(body.Small(self.planet.rect.center))
                            self.planet.kill()
                        elif response:
                            for k in range(random.randint(5, 10)):
                                self.explode_group.add(body.Small(i.rect.center))
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

            if not self.planet.alive:
                font = pygame.font.SysFont('Arial', 60)
                textsurf = font.render('Game Over Press R to Restart', True, (255, 255, 255))
                rect = textsurf.get_rect()
                rect.center = self.surface.get_rect().center
                self.surface.blit(textsurf, rect)

            pygame.display.update()
            self.clock.tick(self.fps)

        if self.restart:
            self.restart = False
            self.start()

    def menu_loop(self):
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    menu_running = False
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        menu_running = False

            self.mouse.update()

            # self.menu.update(self.mouse)

            self.buttons[0].update(self.mouse)
            self.buttons[1].update(self.mouse)

            self.surface.fill((0, 0, 0))

            self.small_group.draw(self.surface)
            self.medium_group.draw(self.surface)
            self.large_group.draw(self.surface)
            self.explode_group.draw(self.surface)
            self.planet.draw(self.surface)

            # self.menu.draw(self.surface)
            self.buttons[0].draw(self.surface)
            self.buttons[1].draw(self.surface)

            self.mouse.draw(self.surface)

            # if self.menu.get("Resume").pressed:
            #     menu_running = False
            # elif self.menu.get("Restart").pressed:
            #     self.start()

            pygame.display.update()

    def spawn(self):
        if time.time() - self.time_init > self.wait:
            self.time_init = time.time()
            self.wait = random.uniform(0, 4)
            type = random.choices(("large", "medium", "small"), cfg.spawn_rate)
            type = type[0]

            if type == "large":
                self.large_group.add(body.Large())
            elif type == "medium":
                self.medium_group.add(body.Medium())
            elif type == "small":
                self.small_group.add(body.Small())

    def larges(self):
        return self.large_group.sprites()

    def mediums(self):
        return self.medium_group.sprites()

    def smalls(self):
        return self.small_group.sprites()

    def start(self):
        self.__init__()


main = Main()