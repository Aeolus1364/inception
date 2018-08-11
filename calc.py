import math
import cfg
import pygame
import random


def grav_acc(loc1, loc2, mass, negative=False):
    x_diff = loc2[0] - loc1[0]
    y_diff = loc2[1] - loc1[1]

    dist = math.sqrt(x_diff ** 2 + y_diff ** 2)
    ang = math.degrees(math.atan2(y_diff, x_diff))

    try:
        acc = (cfg.grav_const * mass) / (dist ** 2)
    except ZeroDivisionError:
        acc = cfg.max_acc

    if acc > cfg.max_acc:
        acc = cfg.max_acc

    if negative:
        acc = -acc

    x_acc = acc * math.cos(math.radians(ang))
    y_acc = acc * math.sin(math.radians(ang))

    return x_acc, y_acc


def grav_iter(sprites, obj, no_touch=False, negative=False):
    if no_touch:
        for i in sprites:
            if not circ_coll(i, obj):
                acc = grav_acc(i.rect.center, obj.rect.center, obj.mass, negative)
                i.x_acc += acc[0]
                i.y_acc += acc[1]
    else:
        for i in sprites:
            acc = grav_acc(i.rect.center, obj.rect.center, obj.mass, negative)
            i.x_acc += acc[0]
            i.y_acc += acc[1]


def circ_coll(obj1, obj2):
    dist = math.hypot(obj1.rect.centerx - obj2.rect.centerx, obj1.rect.centery - obj2.rect.centery)
    if dist < obj1.radius + obj2.radius:
        return True
    else:
        return False


def outcome(obj1, obj2):
    tmass = obj1.mass + obj2.mass
    mdiff = obj1.mass / tmass - obj2.mass / tmass

    big = obj1
    sml = obj2

    if mdiff < 0:
        big = obj2
        sml = obj1

    mdiff = abs(mdiff)

    print(mdiff)

    if mdiff > 0.3:
        big.add(1 - mdiff * sml.mass)
        sml.mark()




def vect2grid(mag, ang):
    x = mag * math.cos(math.radians(ang))
    y = mag * math.sin(math.radians(ang))

    return x, y


def clean_up(objs):
    for obj in objs:
        if obj.rect.x > cfg.dim[0] + cfg.kill_dist or obj.rect.x < 0 - cfg.kill_dist:
            obj.kill()
        if obj.rect.y > cfg.dim[1] + cfg.kill_dist or obj.rect.y < (0 - cfg.kill_dist):
            obj.kill()


def resize(rect, image, factor):
    center = rect.center
    size = int(rect.w * factor), int(rect.h * factor)
    image = pygame.transform.scale(image, size)
    rect = image.get_rect()
    rect.center = center
    return rect, image


# def weighted_choices(choices, weights):
#     total = 0
#     weights_c = []
#     holder = 0
#     for i in weights:
#         total += i
#     for i in weights:
#         weights_c.append(i/total)
#     rand = random.uniform(0, 1)
#     for i in range(len(weights_c)):
#         print(rand, holder, weights_c[i] + holder)
#         if holder < rand < holder + weights_c[i]:
#             return choices[i]
#         else:
#             holder = holder + weights_c[i]