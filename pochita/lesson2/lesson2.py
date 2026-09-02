"""Lesson 2 — Bread and jam.

    ./venv/bin/python pochita/lesson2/lesson2.py     (from python-games)

Arrow keys move him.  ESC or close the window to quit.

Lesson 1 was a film: Pochita walked because a number told him to, and you
watched. This one is a game, and the difference is you. Same YOUR CODE block,
same machinery underneath — but now the machinery asks what you're holding
down, sixty times a second, and hands the answer to your code.

Fetch Denji some bread AND some jam and he'll come out and eat. One of the two
you can reach. The other one you can't, and working out why is the lesson.
"""

# ===========================================================================
#  YOUR CODE
#  Change a number. Save the file. Run it again. See what happened.
# ===========================================================================

SPEED = 4            # pixels he moves each frame while you hold a key

SIZE = 3             # how big to draw him. Whole numbers only (1, 2, 3...)

REACH = 50           # how close his middle has to get to a thing's middle
                     # before he can pick it up

NEEDED = 1           # how many of EACH he has to fetch before Denji comes out

BACKGROUND = (246, 234, 220)     # (red, green, blue), each 0 to 255

WIN_MESSAGE = "Thanks Evolett, you made my dream come true of eating toast with jam!"


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

import math
import os
import random

import pygame

WIDTH = 900
HEIGHT = 600

HERE = os.path.dirname(os.path.abspath(__file__))
POCHITA = os.path.dirname(HERE)                     # the folder one level up
SPRITES = os.path.join(POCHITA, "sprites")          # every lesson shares this

if not os.path.isdir(SPRITES):
    raise SystemExit(
        "\nCan't find the 'sprites' folder.\n"
        "It should sit in the pochita folder, one level up from this file.\n")

if not isinstance(SIZE, int) or SIZE < 1:
    raise SystemExit(
        "\nSIZE is %r. It has to be a whole number, 1 or more.\n"
        "It's how many times bigger than the original drawing to make him.\n"
        % (SIZE,))

if (not isinstance(BACKGROUND, (tuple, list)) or len(BACKGROUND) != 3
        or not all(isinstance(c, int) and 0 <= c <= 255 for c in BACKGROUND)):
    raise SystemExit(
        "\nBACKGROUND is %r.\n"
        "It needs three whole numbers between 0 and 255, like (246, 234, 220)\n"
        "— one each for red, green and blue.\n" % (BACKGROUND,))

if not isinstance(REACH, (int, float)) or not 1 <= REACH <= 200:
    raise SystemExit(
        "\nREACH is %r. It has to be between 1 and 200.\n"
        "Any bigger and he'd be touching a thing the moment it appeared,\n"
        "which would hand you the whole game without you moving.\n" % (REACH,))

if not isinstance(NEEDED, int) or NEEDED < 1:
    raise SystemExit(
        "\nNEEDED is %r. It has to be a whole number, 1 or more.\n"
        "It's how many of each thing Pochita has to fetch before Denji\n"
        "comes out — and at 0 he'd come out before you'd done anything.\n"
        % (NEEDED,))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lesson 2 — Bread and jam")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 26)
big_font = pygame.font.Font(None, 34)
title_font = pygame.font.Font(None, 38)
button_font = pygame.font.Font(None, 32)


class Keys(dict):
    """A dict that explains itself when you ask it something odd."""

    def __missing__(self, name):
        raise SystemExit(
            "\nThere's no key called %r.\n"
            "The four you can ask about are: left, right, up, down.\n"
            "They're all lowercase — check your spelling.\n" % (name,))

    def __getattr__(self, name):
        if name.startswith("__"):            # Python's own private questions
            raise AttributeError(name)
        raise SystemExit(
            "\nYou wrote  keys.%s  — it needs square brackets and quotes:\n"
            '\n    keys["%s"]\n' % (name, name))


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

BREAD_W, BREAD_H = 46, 36        # wide: you run at it sideways
JAM_W, JAM_H = 32, 46            # tall: you have to go up or down for it
MARGIN = 60


def new_bread(px, py):
    """Bread lands further along the same row Pochita is standing on.

    It has to land outside REACH, or he'd pick the new one up the instant it
    appeared and keep doing that forever. If nothing far enough turns up we
    use the furthest spot we saw.
    """
    far = max(260, REACH + 40)
    best, best_gap = MARGIN, -1
    for _ in range(120):
        bx = random.randint(MARGIN, WIDTH - MARGIN)
        gap = abs(bx - px)
        if gap > best_gap:
            best, best_gap = bx, gap
        if gap > far:
            return bx, py
    return best, py


def new_jam(px, py):
    """Jam lands further up or down the same column Pochita is standing in."""
    far = max(170, REACH + 40)
    best, best_gap = MARGIN, -1
    for _ in range(120):
        jy = random.randint(MARGIN, HEIGHT - MARGIN)
        gap = abs(jy - py)
        if gap > best_gap:
            best, best_gap = jy, gap
        if gap > far:
            return px, jy
    return px, best


def draw_bread(cx, cy, scale=1.0):
    crust = pygame.Rect(0, 0, int(BREAD_W * scale), int(BREAD_H * scale))
    crust.center = (cx, cy)
    pygame.draw.rect(screen, (196, 142, 74), crust, border_radius=9)
    inner = crust.inflate(-10 * scale, -10 * scale)
    pygame.draw.rect(screen, (238, 206, 150), inner, border_radius=6)


def draw_jam(cx, cy, scale=1.0):
    w, h = int(JAM_W * scale), int(JAM_H * scale)
    body = pygame.Rect(0, 0, w, h - int(12 * scale))
    body.center = (cx, cy + 6 * scale)
    pygame.draw.rect(screen, (162, 38, 54), body, border_radius=7)
    inner = body.inflate(-10 * scale, -12 * scale)
    pygame.draw.rect(screen, (218, 72, 90), inner, border_radius=5)
    lid = pygame.Rect(0, 0, w + int(6 * scale), int(13 * scale))
    lid.center = (cx, cy - h // 2 + 7 * scale)
    pygame.draw.rect(screen, (126, 98, 64), lid, border_radius=4)


DENJI_HAIR = (236, 201, 96)
DENJI_HAIR_DARK = (196, 158, 58)
DENJI_SKIN = (250, 214, 180)
DENJI_LINE = (54, 42, 38)
DENJI_SHIRT = (246, 246, 242)
DENJI_TIE = (58, 52, 64)
BREAD_CRUMB = (196, 142, 74)
JAM_CRUMB = (196, 52, 70)

CRUMB_SECONDS = 0.7


def denji_surface(chomp):
    """A small Denji. `chomp` is 0 for mouth shut, 1 for mouth wide open."""
    w, h = 36, 56
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    cx = w // 2

    body = pygame.Rect(cx - 11, 34, 22, 20)
    pygame.draw.rect(surf, DENJI_SHIRT, body, border_radius=4)
    pygame.draw.rect(surf, DENJI_LINE, body, width=1, border_radius=4)
    pygame.draw.polygon(surf, DENJI_TIE,
                        [(cx, 35), (cx - 3, 41), (cx, 52), (cx + 3, 41)])

    head = pygame.Rect(cx - 12, 12, 24, 25)
    pygame.draw.ellipse(surf, DENJI_SKIN, head)
    pygame.draw.ellipse(surf, DENJI_LINE, head, width=1)

    mouth = pygame.Rect(cx - 5, 27, 10, 2 + int(7 * chomp))
    pygame.draw.ellipse(surf, (122, 44, 48), mouth)
    pygame.draw.ellipse(surf, DENJI_LINE, mouth, width=1)

    pygame.draw.ellipse(surf, DENJI_LINE, pygame.Rect(cx - 7, 23, 3, 4))
    pygame.draw.ellipse(surf, DENJI_LINE, pygame.Rect(cx + 4, 23, 3, 4))

    # hair: the cap first, then spikes on top of it so they actually show
    cap = pygame.Rect(cx - 13, 9, 26, 13)
    pygame.draw.ellipse(surf, DENJI_HAIR, cap)
    for dx, tall in ((-11, 7), (-6, 11), (0, 12), (6, 11), (11, 7)):
        pygame.draw.polygon(surf, DENJI_HAIR,
                            [(cx + dx - 5, 14), (cx + dx, 14 - tall),
                             (cx + dx + 5, 14)])
    pygame.draw.ellipse(surf, DENJI_HAIR_DARK, cap, width=1)
    return surf


# built once, big, because he's the reward and should fill some space
DENJI_BIG = [pygame.transform.scale(denji_surface(i / 5.0), (108, 168))
             for i in range(6)]

crumbs = []          # little bursts left behind when something gets picked up


def spawn_crumbs(cx, cy, kind, when):
    crumbs.append({
        "x": cx, "y": cy, "kind": kind, "born": when,
        "bits": [(random.uniform(-1.0, 1.0), random.uniform(-1.5, -0.3))
                 for _ in range(8)],
    })


def draw_crumbs(when):
    for c in crumbs[:]:
        age = (when - c["born"]) / 1000.0
        if age >= CRUMB_SECONDS:
            crumbs.remove(c)
            continue
        along = age / CRUMB_SECONDS
        colour = BREAD_CRUMB if c["kind"] == "bread" else JAM_CRUMB
        for vx, vy in c["bits"]:
            px = c["x"] + vx * 86 * along
            py = c["y"] - 44 + vy * 86 * along + 150 * along * along
            size = max(1, int(5 * (1.0 - along)))
            pygame.draw.circle(screen, colour, (int(px), int(py)), size)


def wrap(text, a_font, max_width):
    """Break a long line into several that each fit across the screen."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if not line or a_font.size(trial)[0] <= max_width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def win_layout():
    """Where everything on the finished-the-game screen goes.

    A long WIN_MESSAGE pushes the picture and the button down. Past a point
    there's no room left, so the message gets trimmed rather than shoving
    Denji off the bottom of the window — he's the whole reward.
    """
    lines = wrap(WIN_MESSAGE, title_font, WIDTH - 150)
    tall = DENJI_BIG[0].get_height()
    text_top = 84
    denji_top = text_top + len(lines) * 42 + 26
    button = pygame.Rect(0, 0, 230, 60)
    button.centerx = WIDTH // 2
    button.top = denji_top + tall + 28
    if button.bottom > HEIGHT - 16:
        button.bottom = HEIGHT - 16
        denji_top = button.top - 28 - tall
        room = max(1, (denji_top - 26 - text_top) // 42)
        lines = lines[:room]
    return lines, text_top, denji_top, button


def draw_win_screen(when, mouse_pos):
    """A see-through sheet over the game, with Denji finally eating."""
    veil = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    veil.fill((26, 18, 13, 238))
    screen.blit(veil, (0, 0))

    lines, text_top, denji_top, button = win_layout()

    for i, line in enumerate(lines):
        art = title_font.render(line, True, (252, 246, 238))
        screen.blit(art, ((WIDTH - art.get_width()) // 2, text_top + i * 42))

    chomp = abs(math.sin(when / 1000.0 * 9.0))
    denji = DENJI_BIG[min(5, int(chomp * 5.99))]
    screen.blit(denji, ((WIDTH - denji.get_width()) // 2, denji_top))

    # a slice of bread on one side of him and the jam on the other
    bob = math.sin(when / 1000.0 * 3.0) * 5
    food_y = denji_top + denji.get_height() // 2
    draw_bread(WIDTH // 2 - 132, int(food_y + bob), 1.5)
    draw_jam(WIDTH // 2 + 132, int(food_y - bob), 1.5)

    hot = button.collidepoint(mouse_pos)
    pygame.draw.rect(screen, (250, 226, 168) if hot else (232, 200, 132),
                     button, border_radius=12)
    pygame.draw.rect(screen, (120, 92, 48), button, width=2, border_radius=12)
    label = button_font.render("Play again", True, (58, 44, 32))
    screen.blit(label, (button.centerx - label.get_width() // 2,
                        button.centery - label.get_height() // 2))
    return button


def draw_floor():
    screen.fill(BACKGROUND)
    tile = 60
    faint = (236, 223, 208)
    for gx in range(0, WIDTH, tile):
        pygame.draw.line(screen, faint, (gx, 0), (gx, HEIGHT))
    for gy in range(0, HEIGHT, tile):
        pygame.draw.line(screen, faint, (0, gy), (WIDTH, gy))


x = y = 0.0
bread_got = jam_got = 0
bread_x = bread_y = jam_x = jam_y = 0
won = False


def start_round():
    """Put everything back for a fresh go."""
    global x, y, bread_got, jam_got, bread_x, bread_y, jam_x, jam_y, won
    x = WIDTH / 2.0
    y = HEIGHT / 2.0
    bread_got = 0
    jam_got = 0
    bread_x, bread_y = new_bread(x, y)
    jam_x, jam_y = new_jam(x, y)
    won = False
    crumbs.clear()


start_round()
facing = "right"
frame = 0
last_frame_change = 0

running = True
while running:
    now = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif won and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                start_round()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and won:
            if win_layout()[3].collidepoint(event.pos):
                start_round()

    if not won:
        held = pygame.key.get_pressed()
        keys = Keys(
            left=held[pygame.K_LEFT] or held[pygame.K_a],
            right=held[pygame.K_RIGHT] or held[pygame.K_d],
            up=held[pygame.K_UP] or held[pygame.K_w],
            down=held[pygame.K_DOWN] or held[pygame.K_s],
        )

        was_x, was_y = x, y

        try:
            result = move(x, y, keys)
        except NameError as problem:
            raise SystemExit(
                "\nmove() uses a name Python doesn't know: %s\n"
                "\nIf you meant one of the arrow keys, it needs BOTH quotes and\n"
                "square brackets:\n"
                '\n    keys["up"]        not   keys[up]\n'
                "\nAnd names have to match exactly: SPEED is not the same as speed.\n"
                % (problem,))
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

        try:
            got_bread = is_touching(x, y, bread_x, bread_y)
            got_jam = is_touching(x, y, jam_x, jam_y)
        except NameError as problem:
            raise SystemExit(
                "\nis_touching() uses a name Python doesn't know: %s\n"
                "\nNames have to match exactly, and the four it is handed are\n"
                "called ax, ay, bx and by.\n" % (problem,))
        if got_bread is None or got_jam is None:
            raise SystemExit(
                "\nis_touching() didn't hand anything back.\n"
                "It needs to end with a `return`, and hand back True or False.\n")
        if got_bread:
            bread_got = bread_got + 1
            spawn_crumbs(bread_x, bread_y, "bread", now)
            bread_x, bread_y = new_bread(x, y)
        if got_jam:
            jam_got = jam_got + 1
            spawn_crumbs(jam_x, jam_y, "jam", now)
            jam_x, jam_y = new_jam(x, y)

        if bread_got >= NEEDED and jam_got >= NEEDED:
            won = True

    draw_floor()
    draw_bread(bread_x, bread_y)
    draw_jam(jam_x, jam_y)
    screen.blit(WALK[facing][frame],
                (int(x - POCHITA_W / 2), int(y - POCHITA_H / 2)))
    draw_crumbs(now)

    if won:
        draw_win_screen(now, mouse_pos)
    else:
        screen.blit(big_font.render("bread %d / %d     jam %d / %d"
                                    % (bread_got, NEEDED, jam_got, NEEDED),
                                    True, (120, 100, 88)), (16, 14))
        screen.blit(font.render("x = %d    y = %d" % (x, y),
                               True, (168, 150, 136)), (16, 50))
        holding = " ".join(n for n in ("left", "right", "up", "down") if keys[n])
        screen.blit(font.render("holding: %s" % (holding or "nothing"),
                               True, (168, 150, 136)), (16, 74))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
