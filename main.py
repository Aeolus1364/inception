import pygame
import body
import cfg
import calc
import random
import time
import res
import menu
import sys

pygame.init()
pygame.mixer.music.load("res/music.wav")
pygame.mixer.music.play(-1)

cfg.init()

started = False
fullscreen = False


class Main:
    def __init__(self):
        global started
        global fullscreen
        self.data = pygame.display.Info()
        self.max_res = self.data.current_w, self.data.current_h
        self.min_res = cfg.dim

        pygame.display.set_caption("Inception")
        pygame.display.set_icon(res.asteroid)
        pygame.mouse.set_visible(False)

        self.running = True
        self.clock = pygame.time.Clock()

        if fullscreen:
            self.surface = pygame.display.set_mode(cfg.dim, pygame.FULLSCREEN)
        else:
            self.surface = pygame.display.set_mode(cfg.dim)


        self.fps = 30
        self.fullscreen = False
        self.midpoint = (cfg.dim[0] / 2, cfg.dim[1] / 2)

        self.mouse = body.Mouse()

        buttons = [
            menu.Button("Start", 30, (self.midpoint[0], self.midpoint[1] - 150)),
            menu.Button("Settings", 30, (self.midpoint[0], self.midpoint[1] - 75)),
            menu.Button("Controls", 30, (self.midpoint[0], self.midpoint[1])),
            menu.Button("Credits", 30, (self.midpoint[0], self.midpoint[1] + 75)),
            menu.Button("Quit", 30, (self.midpoint[0], self.midpoint[1] + 150))
        ]

        if not started:
            self.res_button = menu.CycleButton(("1280 x 800", "1920 x 1080"), 30, (self.midpoint[0], self.midpoint[1] - 75))
            self.windowed_button = menu.CycleButton(("Windowed", "Fullscreen"), 30, (self.midpoint[0], self.midpoint[1]))
            started = True

        self.apply_button = menu.Button("Apply", 30, (self.midpoint[0], self.midpoint[1] + 75))
        self.res_button.center = (self.midpoint[0], self.midpoint[1] - 75)
        self.windowed_button.center = (self.midpoint[0], self.midpoint[1])

        self.main_menu = menu.Menu(buttons)

        self.main_menu_loop()

        self.multi_init()

    def multi_init(self):
        self.time_init = time.time()
        self.wait = 0

        self.objects = body.Group()
        self.planet = body.Planet()

        # for i in range(50):
        #     self.objects.add(body.Object())

        buttons = [
            menu.Button("Resume", 30, (self.midpoint[0], self.midpoint[1] - 150)),
            menu.Button("Restart", 30, (self.midpoint[0], self.midpoint[1] - 75)),
            menu.Button("Controls", 30, (self.midpoint[0], self.midpoint[1])),
            menu.Button("Main Menu", 30, (self.midpoint[0], self.midpoint[1] + 75)),
            menu.Button("Quit", 30, (self.midpoint[0], self.midpoint[1] + 150))
        ]

        self.pause_menu = menu.Menu(buttons)

        self.restart_button = menu.Button("Restart?", 30, (self.midpoint[0], self.midpoint[1] + 50))

        self.main_loop()

    def main_loop(self):
        grav_on = False
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        self.running = False
                    if event.key == pygame.K_ESCAPE:
                        if self.planet.alive:
                            self.pause_menu_loop()
                    if event.key == pygame.K_r:
                        self.start()
                    if event.key == pygame.K_SPACE:
                        self.objects.add(body.Object(50, self.mouse.pos()))
                    if event.key == pygame.K_LEFT:
                        self.objects.add(body.Object(50, self.mouse.pos()))

                    if event.key == pygame.K_RIGHT:
                        self.objects.add(body.Object(500, self.mouse.pos()))

            if self.mouse.state:
                grav_on = True
            else:
                grav_on = False

            self.mouse.mass = self.planet.mass

            if grav_on:
                calc.grav_iter(self.objects.sprites(), self.mouse, True)
            if self.planet.alive:
                calc.grav_iter(self.objects.sprites(), self.planet)

            for i in self.objects.sprites():
                if calc.circ_coll(i, self.planet):
                    self.planet.add(i.mass)
                    i.kill()

            self.objects.update()
            self.mouse.update()

            self.surface.fill((0, 0, 0))

            self.objects.draw(self.surface)
            self.planet.draw(self.surface)

            self.spawn()

            if not self.planet.alive:
                font = pygame.font.SysFont('Arial', 60)
                textsurf = font.render('Game Over', True, (255, 255, 255))
                rect = textsurf.get_rect()
                rect.centerx = self.surface.get_rect().centerx
                rect.centery = self.surface.get_rect().centery - 50
                self.surface.blit(textsurf, rect)
                self.restart_button.update(self.mouse)
                self.restart_button.draw(self.surface)
                if self.restart_button.action():
                    self.start()

            self.mouse.draw(self.surface)

            # self.spawn()

            calc.clean_up(self.objects)

            pygame.display.update()
            self.clock.tick(self.fps)

    def main_menu_loop(self):
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            if self.main_menu.get("Start").action():
                menu_running = False
            elif self.main_menu.get("Quit").action():
                self.quit()
            elif self.main_menu.get("Settings").action():
                self.settings_menu()
                self.__init__()

            self.mouse.update()
            self.main_menu.update(self.mouse)

            self.surface.fill((0, 0, 0))

            font = pygame.font.SysFont("Arial", 100)
            render = font.render("Interstellar Inception", True, (255, 255, 255))
            fontrect = render.get_rect()
            fontrect.centerx = self.midpoint[0]
            fontrect.y = 50

            self.surface.blit(render, fontrect)

            self.main_menu.draw(self.surface)
            self.mouse.draw(self.surface)

            pygame.display.update()
            self.clock.tick(self.fps)

    def settings_menu(self):
        global fullscreen
        menu_running = True
        while menu_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

            self.mouse.update()
            self.res_button.update(self.mouse)
            self.windowed_button.update(self.mouse)
            self.apply_button.update(self.mouse)
            self.res_button.action()
            self.windowed_button.action()

            if self.apply_button.action():
                menu_running = False
                # self.menu()

                res = self.res_button.get_text()
                if res == "1280 x 800":
                    cfg.dim = (1280, 800)
                elif res == "1920 x 1080":
                    cfg.dim = (1920, 1080)

                wind = self.windowed_button.get_text()
                if wind == "Windowed":
                    fullscreen = False
                elif wind == "Fullscreen":
                    fullscreen = True

            self.surface.fill((0, 0, 0))

            font = pygame.font.SysFont("Arial", 100)
            render = font.render("Interstellar Inception", True, (255, 255, 255))
            fontrect = render.get_rect()
            fontrect.centerx = self.midpoint[0]
            fontrect.y = 50

            self.surface.blit(render, fontrect)

            self.res_button.draw(self.surface)
            self.windowed_button.draw(self.surface)
            self.apply_button.draw(self.surface)
            self.mouse.draw(self.surface)

            pygame.display.update()
            self.clock.tick(self.fps)

    def pause_menu_loop(self):
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

            self.pause_menu.update(self.mouse)

            self.surface.fill((0, 0, 0))

            self.objects.draw(self.surface)
            self.planet.draw(self.surface)

            self.pause_menu.draw(self.surface)

            self.mouse.draw(self.surface)

            if self.pause_menu.get("Resume").action():
                menu_running = False
            elif self.pause_menu.get("Restart").action():
                self.start()
                menu_running = False
            elif self.pause_menu.get("Controls").action():
                pass
            elif self.pause_menu.get("Main Menu").action():
                self.menu()
            elif self.pause_menu.get("Quit").action():
                self.quit()

            pygame.display.update()

    def spawn(self):
        if time.time() - self.time_init > self.wait:
            self.time_init = time.time()
            self.wait = random.uniform(0, 4)
            self.objects.add(body.Object(random.randint(int(self.planet.mass / 10), int(self.planet.mass * 1.5))))

    def start(self):
        self.multi_init()

    def menu(self):
        self.main_menu_loop()
        self.multi_init()

    def quit(self):
        pygame.quit()
        sys.exit()


main = Main()
