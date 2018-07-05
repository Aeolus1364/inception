import pygame


def load(image):
    img = pygame.image.load(image)
    dim = img.get_size()
    dim = (dim[0]*2, dim[1]*2)
    img = pygame.transform.scale(img, dim)
    return img


button_unpressed = load("res/button_u.png")
button_pressed = load("res/button_p.png")
mouse_unclicked = load("res/mouse1t.png")
mouse_clicked = load("res/mouse2t.png")
meteoroid = load("res/meteoroid.png")
asteroid = load("res/asteroid.png")
planet = load("res/planet.png")
roundy = load("res/planet2.png")
planetoid = load("res/planetoid.png")
gasgiant = load("res/gasgiant.png")
star = load("res/star.png")


