SPEED = 4        # pixels per frame while you hold a key
SIZE = 3         # how big to draw him
REACH = 50       # how close he has to get to grab something
NEEDED = 1       # how many of each before Denji comes out
BACKGROUND = (246, 234, 220)

WIN_MESSAGE = "Thanks Evolett, you made my dream come true of eating toast with jam!"


def move(x, y, keys):
    if keys["left"]:
        x = x - SPEED

    if keys["right"]:
        x = x + SPEED

    # your turn goes here

    return x, y


def is_touching(ax, ay, bx, by):
    return abs(ax - bx) < REACH and abs(ay - by) < REACH
