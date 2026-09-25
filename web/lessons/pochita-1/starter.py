SPEED = 3        # pixels per frame
POCHITA_Y = 305  # how far down he is
SIZE = 5         # how big to draw him
FRAME_MS = 140   # how long each leg drawing is held
BACKGROUND = (246, 234, 220)


def move(x, speed):
    x = x + speed

    # your turn goes here

    return x, speed
