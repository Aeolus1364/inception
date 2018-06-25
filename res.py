import pygame


def load(image):
    img = pygame.image.load(image)
    img = pygame.transform.scale2x(img)
    return img


mouse_unclicked = load("res/mouse1.png")
mouse_clicked = load("res/mouse2.png")
button = load("res/button.png")
meteoroid = load("res/meteoroid.png")
asteroid = load("res/asteroid.png")
planet = load("res/planet.png")
planetoid = load("res/planetoid.png")


