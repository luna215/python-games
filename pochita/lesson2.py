"""Lesson 2 — Pochita goes looking for bread.

    ./venv/bin/python pochita/lesson2.py      (from the python-games folder)

Arrow keys move him.  ESC or close the window to quit.

Lesson 1 was a film: Pochita walked because a number told him to, and you
watched. This one is a game, and the difference is you. Same YOUR CODE block,
same machinery underneath — but now the machinery asks what you're holding
down, sixty times a second, and hands the answer to your code.
"""

# ===========================================================================
#  YOUR CODE
#  Change a number. Save the file. Run it again. See what happened.
# ===========================================================================

SPEED = 4            # pixels he moves each frame while you hold a key

SIZE = 3             # how big to draw him. Whole numbers only (1, 2, 3...)

REACH = 50           # how close his middle has to get to the bread's middle
                     # before he can eat it

BACKGROUND = (246, 234, 220)     # (red, green, blue), each 0 to 255


def move(x, y, keys):
    """Where should Pochita be next?

    Runs 60 times a second. `x` and `y` are where the MIDDLE of him is right
    now. `keys` tells you what's held down at this instant — `keys["left"]`
    is either True or False.

    Hand back both numbers and the machinery draws him there.
    """

    if keys["left"]:
        x = x - SPEED

    if keys["right"]:
        x = x + SPEED

    # ------------------------------------------------------------------
    #  YOUR TURN — he only goes left and right. Give him up and down.
    #
    #  Two more `if` statements, the same shape as the two above, using
    #  keys["up"] and keys["down"] — and changing `y` instead of `x`.
    #
    #  One warning, and it's the whole lesson: on a screen, `y` counts
    #  DOWNWARDS from the top. Guess which way is up, try it, and watch
    #  what he actually does before you decide you were right.
    # ------------------------------------------------------------------

    return x, y


def is_touching(ax, ay, bx, by):
    """Are these two things close enough to count as touching?

    (ax, ay) is the middle of one thing and (bx, by) is the middle of the
    other. Hand back True or False.

    `abs()` throws away a minus sign, so `abs(ax - bx)` is how far apart they
    are left-to-right, however you subtract them.
    """

    return abs(ax - bx) < REACH and abs(ay - by) < REACH


# ===========================================================================
#  THE MACHINERY
#  We'll open this up and read it properly in a few weeks.
# ===========================================================================

import os
import random

import pygame

WIDTH = 900
HEIGHT = 600

HERE = os.path.dirname(os.path.abspath(__file__))
SPRITES = os.path.join(HERE, "sprites")

if not os.path.isdir(SPRITES):
    raise SystemExit(
        "\nCan't find the 'sprites' folder.\n"
        "It should sit right next to this file.\n")

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lesson 2 — Pochita goes looking for bread")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 26)
big_font = pygame.font.Font(None, 34)


class Keys(dict):
    """A dict that explains itself when you ask it for a key that isn't there."""

    def __missing__(self, name):
        raise SystemExit(
            "\nThere's no key called %r.\n"
            "The four you can ask about are: left, right, up, down.\n"
            "They're all lowercase — check your spelling.\n" % (name,))


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

BREAD_W, BREAD_H = 46, 36
MARGIN = 60


def new_bread(away_from_x, away_from_y):
    """Drop a piece of bread somewhere else on the floor."""
    for _ in range(80):
        bx = random.randint(MARGIN, WIDTH - MARGIN)
        by = random.randint(MARGIN, HEIGHT - MARGIN)
        far_enough = abs(bx - away_from_x) > 220 or abs(by - away_from_y) > 160
        if far_enough:
            return bx, by
    return WIDTH - MARGIN, HEIGHT - MARGIN


def draw_bread(cx, cy):
    crust = pygame.Rect(0, 0, BREAD_W, BREAD_H)
    crust.center = (cx, cy)
    pygame.draw.rect(screen, (196, 142, 74), crust, border_radius=9)
    inner = crust.inflate(-10, -10)
    pygame.draw.rect(screen, (238, 206, 150), inner, border_radius=6)


def draw_floor():
    screen.fill(BACKGROUND)
    tile = 60
    faint = (236, 223, 208)
    for gx in range(0, WIDTH, tile):
        pygame.draw.line(screen, faint, (gx, 0), (gx, HEIGHT))
    for gy in range(0, HEIGHT, tile):
        pygame.draw.line(screen, faint, (0, gy), (WIDTH, gy))


x = WIDTH / 2.0
y = HEIGHT / 2.0
facing = "right"
frame = 0
last_frame_change = 0
score = 0
bread_x, bread_y = new_bread(x, y)

running = True
while running:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    held = pygame.key.get_pressed()
    keys = Keys(
        left=held[pygame.K_LEFT] or held[pygame.K_a],
        right=held[pygame.K_RIGHT] or held[pygame.K_d],
        up=held[pygame.K_UP] or held[pygame.K_w],
        down=held[pygame.K_DOWN] or held[pygame.K_s],
    )

    was_x, was_y = x, y

    result = move(x, y, keys)
    if result is None:
        raise SystemExit(
            "\nmove() didn't hand anything back.\n"
            "It needs `return x, y` as its last line.\n")
    try:
        x, y = result
    except (TypeError, ValueError):
        raise SystemExit(
            "\nmove() has to hand back exactly two numbers, like `return x, y`.\n"
            "Right now it hands back: %r\n" % (result,))

    # keep him on the floor you can see
    x = max(POCHITA_W / 2, min(WIDTH - POCHITA_W / 2, x))
    y = max(POCHITA_H / 2, min(HEIGHT - POCHITA_H / 2, y))

    moved = abs(x - was_x) > 0.01 or abs(y - was_y) > 0.01
    if x < was_x:
        facing = "left"
    elif x > was_x:
        facing = "right"

    # his legs only move while he does
    if moved and now - last_frame_change >= 120:
        frame = (frame + 1) % 4
        last_frame_change = now
    if not moved:
        frame = 0

    eaten = is_touching(x, y, bread_x, bread_y)
    if eaten is None:
        raise SystemExit(
            "\nis_touching() didn't hand anything back.\n"
            "It needs to end with a `return`, and hand back True or False.\n")
    if eaten:
        score = score + 1
        bread_x, bread_y = new_bread(x, y)

    draw_floor()
    draw_bread(bread_x, bread_y)
    screen.blit(WALK[facing][frame],
                (int(x - POCHITA_W / 2), int(y - POCHITA_H / 2)))

    holding = " ".join(name for name in ("left", "right", "up", "down") if keys[name])
    screen.blit(big_font.render("bread eaten: %d" % score, True, (120, 100, 88)),
                (16, 14))
    screen.blit(font.render("x = %d    y = %d" % (x, y), True, (168, 150, 136)),
                (16, 50))
    screen.blit(font.render("holding: %s" % (holding or "nothing"),
                           True, (168, 150, 136)), (16, 74))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
