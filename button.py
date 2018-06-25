import pygame
import res


class Button(pygame.sprite.Sprite):
    def __init__(self, center, text):
        super(Button, self).__init__()

        self.image = res.button
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.text = Text(text)

        self.text.rect.center = self.image.get_rect().center
        print(self.rect, self.text.rect)
        self.image.blit(self.text.image, self.text.rect)

        # pygame.font.init()
        # self.font = pygame.font.SysFont('Arial', 30)
        # textsurf = self.font.render('Test', True, (0, 0, 0))
        # self.image.blit(textsurf, (0, 0))

    def collide(self, point):
        if self.rect.collidepoint(point):
            return True
        else:
            return False


class Text(pygame.sprite.Sprite):
    def __init__(self, text):
        super(Text, self).__init__()
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 30)
        self.image = self.font.render(text, True, (0, 0, 0))
        self.rect = self.image.get_rect()

        print(self.rect)