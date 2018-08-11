dim, spawn_dist, kill_dist, spawn_ang, grav_const, max_acc, min_ratio, mult_ratio, coll_thresh = 0, 0, 0, 0, 0, 0, 0, 0, 0


def init():
    global dim, spawn_dist, kill_dist, spawn_ang, grav_const, max_acc, min_ratio, max_ratio, mult_ratio, spawn_rate, coll_thresh
    dim = (800, 800)
    spawn_dist = 200
    kill_dist = 500
    spawn_ang = 60
    grav_const = 1
    max_acc = 5
    min_ratio = 0.1
    max_ratio = 1.5
    mult_ratio = 0.5
    coll_thresh = 0.3


