"""Lesson 1 — Pochita goes for a walk.

    ./venv/bin/python pochita/lesson1/lesson1.py     (from python-games)

ESC or close the window to quit.

This is the first thing you'll run on your own machine instead of in a browser.
Same idea as before: everything you change lives in the YOUR CODE block. The
machinery underneath opens the window and redraws it sixty times a second.
"""

# ===========================================================================
#  YOUR CODE
#  Change a number. Save the file. Run it again. See what happened.
# ===========================================================================

SPEED = 3            # pixels he moves each frame.
                     # Try a negative number and see what happens.

POCHITA_Y = 305      # how far DOWN the screen he walks.
                     # At SIZE 5 this puts his feet right on the ground.

SIZE = 5             # how big to draw him. Whole numbers only (1, 2, 3...)

FRAME_MS = 140       # how long each drawing of his legs is held, in
                     # milliseconds. 1000 milliseconds = 1 second.

BACKGROUND = (246, 234, 220)     # (red, green, blue), each 0 to 255


def move(x, speed):
    """Where should Pochita be next?

    This runs 60 times a second. `x` is where he is now and `speed` is how
    fast he's going. Hand back both, and the machinery uses them.
    """

    x = x + speed

    # ------------------------------------------------------------------
    #  YOUR TURN — right now he walks off the edge and reappears on the
    #  other side. Make him turn around instead.
    #
    #  You need two `if` statements:
    #    if he's gone off the RIGHT edge  -> make speed negative
    #    if he's gone off the LEFT edge   -> make speed positive
    #
    #  The screen is 900 wide. Pochita is about 45 * SIZE pixels wide.
    #  `-speed` means "the same speed, the other way".
    # ------------------------------------------------------------------

    return x, speed


# ===========================================================================
#  THE MACHINERY
#  We'll open this up and read it properly in a few weeks.
# ===========================================================================

import os

import pygame

WIDTH = 900
HEIGHT = 500
GROUND = 60          # how much floor to draw under him

HERE = os.path.dirname(os.path.abspath(__file__))
POCHITA = os.path.dirname(HERE)                     # the folder one level up
SPRITES = os.path.join(POCHITA, "sprites")          # every lesson shares this

if not os.path.isdir(SPRITES):
    raise SystemExit(
        "\nCan't find the 'sprites' folder.\n"
        "It should sit in the pochita folder, one level up from this file.\n")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lesson 1 — Pochita goes for a walk")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 26)


def load_walk(side):
    """The four pictures of Pochita walking one way, blown up by SIZE."""
    frames = []
    for n in (1, 2, 3, 4):
        path = os.path.join(SPRITES, "pochita_%s_%d.png" % (side, n))
        if not os.path.exists(path):
            raise SystemExit("\nMissing sprite: %s\n" % path)
        art = pygame.image.load(path).convert_alpha()
        big = pygame.transform.scale(          # nearest-neighbour keeps it crisp
            art, (art.get_width() * SIZE, art.get_height() * SIZE))
        frames.append(big)
    return frames


WALK = {"left": load_walk("left"), "right": load_walk("right")}
POCHITA_W = WALK["left"][0].get_width()
POCHITA_H = WALK["left"][0].get_height()

x = 100.0
speed = SPEED
frame = 0
last_frame_change = 0

running = True
while running:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    result = move(x, speed)
    if result is None:
        raise SystemExit(
            "\nmove() didn't hand anything back.\n"
            "It needs `return x, speed` as its last line.\n")
    x, speed = result

    # if nobody turned him around, wrap him to the other side
    if x > WIDTH:
        x = -POCHITA_W
    elif x < -POCHITA_W:
        x = WIDTH

    # hold each drawing of his legs for FRAME_MS before moving to the next
    if now - last_frame_change >= max(16, FRAME_MS):
        frame = (frame + 1) % 4
        last_frame_change = now

    facing = "right" if speed > 0 else "left"

    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, (206, 188, 170), (0, HEIGHT - GROUND, WIDTH, GROUND))
    pygame.draw.line(screen, (150, 130, 116),
                     (0, HEIGHT - GROUND), (WIDTH, HEIGHT - GROUND), 3)
    screen.blit(WALK[facing][frame], (int(x), POCHITA_Y))

    hud = font.render("x = %d     speed = %d     facing %s" % (x, speed, facing),
                      True, (120, 100, 88))
    screen.blit(hud, (16, 14))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
