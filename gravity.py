import math
import cfg


def grav_acc(loc1, loc2, mass):
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

    x_acc = acc * math.cos(math.radians(ang))
    y_acc = acc * math.sin(math.radians(ang))

    # print(dist, acc)
    # print(acc, ang)
    # print(x_acc, y_acc)
    # print()

    return x_acc, y_acc


def circ_coll(loc1, rad1, loc2, rad2):
    dist = math.hypot(loc1[0] - loc2[0], loc1[1] - loc2[1])
    if dist < rad1 + rad2:
        return True
    else:
        return False

