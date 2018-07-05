import pygame, res


class Button:
    def __init__(self, text, fs, center):
        self.text = text
        self.surf = res.button_unpressed
        self.rect = self.surf.get_rect()

        self.font = pygame.font.SysFont("Arial", 30)
        self.render = self.font.render(text, False, (0,0,0))

        self.surf.blit(self.render, (0,0))

        self.hover = 0
        self.pressed = 0

    def update(self, mouse):
        self.hover = self.rect.collidepoint(mouse.pos()[0], mouse.pos()[1])
        if self.hover:
            self.pressed = mouse.state
        else:
            self.pressed = 0

    def draw(self, surf):
        surf.blit(self.surf, self.rect)


class Menu:
    def __init__(self, buttons=None):
        if type(buttons) == tuple or list:
            self.buttons = buttons
        elif type(buttons) == Button:
            self.buttons = [buttons]
        else:
            self.buttons = []

    def add(self, obj):
        self.buttons.append(obj)

    def update(self, mouse):
        for i in self.buttons:
            i.update(mouse)

    def draw(self, surface):
        for i in self.buttons:
            surface.blit(i.surf, i.rect)

    def get(self, name):
        for i in self.buttons:
            if i.text == name:
                return i

