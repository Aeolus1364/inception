import pygame, res


class Button:
    def __init__(self, text, fs, center):
        self.text = text
        self.center = center

        self.image_pressed = res.button_pressed.copy()
        self.image_unpressed = res.button_unpressed.copy()

        self.image = self.image_unpressed
        self.rect = self.image.get_rect()

        font = pygame.font.SysFont("Arial", fs)
        render = font.render(text, True, (0, 0, 0))
        fontrect = render.get_rect()
        fontrect.center = self.rect.center

        self.image_pressed.blit(render, fontrect)
        fontrect.y += 1
        fontrect.x -= 1
        self.image_unpressed.blit(render, fontrect)

        self.rect.center = self.center

        self.hover = 0
        self.pressed = 0
        self.clicked = 0
        self.pressed_past = 0

    def update(self, mouse):
        self.hover = self.rect.collidepoint(mouse.pos()[0], mouse.pos()[1])
        self.clicked = mouse.state

        self.pressed_past = self.pressed

        if self.hover and self.clicked:
            self.pressed = True
        else:
            self.pressed = False

        if self.pressed:
            self.image = self.image_pressed
        else:
            self.image = self.image_unpressed

    def draw(self, surf):
        surf.blit(self.image, self.rect)

    def action(self):
        if not self.pressed and self.pressed_past and self.hover:
            return True


class CycleButton(Button):
    def __init__(self, texts, fs, center):
        self.texts = texts
        self.counter = 0
        self.fs = fs
        super().__init__(self.texts[0], self.fs, center)
        print("init")

    def draw(self, surf):
        self.image_pressed = res.button_pressed.copy()
        self.image_unpressed = res.button_unpressed.copy()

        self.rect = self.image.get_rect()

        font = pygame.font.SysFont("Arial", self.fs)
        render = font.render(self.texts[self.counter], True, (0, 0, 0))
        fontrect = render.get_rect()
        fontrect.center = self.rect.center

        self.image_pressed.blit(render, fontrect)
        fontrect.y += 1
        fontrect.x -= 1
        self.image_unpressed.blit(render, fontrect)
        self.rect.center = self.center

        super().draw(surf)

    def get_text(self):
        return self.texts[self.counter]

    def action(self):
        if not self.pressed and self.pressed_past and self.hover:
            if self.counter < len(self.texts) - 1:
                self.counter += 1
            else:
                self.counter = 0
            return True


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
            surface.blit(i.image, i.rect)

    def get(self, name):
        for i in self.buttons:
            if i.text == name:
                return i

