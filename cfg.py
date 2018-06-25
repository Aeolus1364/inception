file = open("settings.txt", "r")
text = file.read().splitlines()
print(text)
for i in text:
    words = i.split(" ")

    if words[0] == "dimensions":
        split = words[2].split("x")
        dim = int(split[0]), int(split[1])
    elif words[0] == "fullscreen":
        fullscreen = words[2]
        if fullscreen == "false":
            fullscreen = False
        elif fullscreen == "true":
            fullscreen = True
        else:
            fullscreen = False

spawn_dist = 200
kill_dist = 500
spawn_ang = 60
grav_const = 100
max_acc = 5
min_ratio = 0.1
max_ratio = 1.5
mult_ratio = 0.5
spawn_rate = (2, 100, 50)