"""
Melody Jumper — a ball that plays a song by landing on it.

Every note in MELODY becomes a platform. High notes sit high up the screen,
low notes sit down low, so the shape of the song is the shape of the level.
The ball jumps along it by itself and plays each note as it lands.

Run it from the python-games folder:

    ./venv/bin/python melody-jumper/jumper.py

SPACE pauses.  R starts the song over.  ESC quits.
"""

import random
import sys

import pygame

import tones


# ============================================================
#  YOUR CODE — everything you change lives up here
# ============================================================

SONG_TITLE = "In the Hall of the Mountain King"

# Beats per minute. Smaller number = slower song.
# 138 is the speed Grieg wrote on the score. The real piece speeds up as it goes
# — try winding this up to 200 and you'll hear why that's the famous part.
TEMPO = 138

# How the notes sound. One of:
#   bell     clean and soft
#   pluck    short and woody
#   lead     detuned and driven
#   heavy    the same, plus an octave underneath
#   searing  square wave, hard distortion
#   moog     three detuned saws that swell in, with an echo
#   solo     distorted, and it slides up into every note
# Try them all. They change the feel more than anything else here.
# "pluck" is here because Grieg marked this tune pizzicato — plucked, not
# bowed. The notes are short and fast, and a voice that rings on for two
# seconds (try "moog") smears them into mush.
VOICE = "pluck"

# The song itself. Each line is ("note name", how many beats it lasts).
#
# Note names are a letter, an optional # (sharp) or b (flat), and an octave
# number. C4 is middle C. C5 is one octave higher. C3 is one octave lower.
# Use "-" for a rest: the ball still lands, but no sound comes out.
#
# "In the Hall of the Mountain King" — Edvard Grieg, 1875, from Peer Gynt.
# Old enough that nobody owns it, so this is the real tune, not something like it.
# Four bars, in B minor, written an octave above where the cellos play it.
#
# Look at bar 2. Every other bar uses notes from B minor, but that one uses F
# and C, which aren't in the key at all. That is the creepy bit, and it is
# deliberate: it's the same three-note shape played twice, the second time one
# semitone lower. Grieg actually wrote the F as "E sharp" — same key on a piano.
MELODY = [
    ("B3", 0.5), ("C#4", 0.5), ("D4", 0.5), ("E4", 0.5), ("F#4", 0.5), ("D4", 0.5), ("F#4", 1),
    ("F4", 0.5), ("C#4", 0.5), ("F4", 1),   ("E4", 0.5), ("C4", 0.5),  ("E4", 1),
    ("B3", 0.5), ("C#4", 0.5), ("D4", 0.5), ("E4", 0.5), ("F#4", 0.5), ("D4", 0.5), ("F#4", 0.5), ("B4", 0.5),
    ("A4", 0.5), ("F#4", 0.5), ("D4", 0.5), ("F#4", 0.5), ("A4", 1),   ("-",  1),
]

BALL_COLOR = (255, 208, 96)
PLATFORM_COLOR = (96, 110, 178)
ACTIVE_COLOR = (255, 238, 186)


def platform_height(note, lowest, highest):
    """
    Decide how high up the screen a platform floats.

    Return 0.0 to put it at the very bottom, 1.0 for the very top,
    0.5 for halfway. Anything in between works too.

    `note` is a number: bigger means a higher-pitched note. `lowest` and
    `highest` are the smallest and biggest numbers in your whole song.
    """
    span = highest - lowest
    if span == 0:
        return 0.5
    return (note - lowest) / span

    # YOUR TURN — try each of these instead of the two lines above.
    #   return 0.5                              (a flat road)
    #   return 1 - (note - lowest) / span       (the song upside down)
    #   return ((note - lowest) / span) ** 3    (only the top notes climb)


# ============================================================
#  THE MACHINERY — you don't have to read this yet
# ============================================================

WIDTH, HEIGHT = 960, 600
PLAY_TOP = 150            # y of the highest a platform can sit
PLAY_BOTTOM = 450         # y of the lowest a platform can sit

GRAVITY = 1900.0          # pixels per second, per second
MAX_AIR = 0.55            # longest time the ball spends in one jump
GAP_PER_SECOND = 260      # how far apart platforms sit, per second of jump
MIN_GAP = 70

BALL_RADIUS = 15
PLATFORM_WIDTH = 96
PLATFORM_HEIGHT = 13
CAMERA_ANCHOR = 0.36      # ball sits this far across the screen

SKY_TOP = (10, 10, 26)
SKY_BOTTOM = (46, 23, 44)
REST_COLOR = (74, 72, 104)
TEXT_COLOR = (150, 152, 190)

# ---------- notes ----------
# The sound itself is built in tones.py, the file this one imports at the top.

def note_number(name):
    """Turn a name like 'C4' or 'F#3' into a number. '-' means silence."""
    try:
        return tones.note_number(name)
    except ValueError as problem:
        raise SystemExit(f"\n{problem}\nCheck your MELODY.\n")


# ---------- laying out the level ----------


def check_melody():
    if len(MELODY) < 2:
        raise SystemExit("\nMELODY needs at least two notes to jump between.\n")

    numbers = []
    for entry in MELODY:
        if not isinstance(entry, (tuple, list)) or len(entry) != 2:
            raise SystemExit(
                f"\nEvery line of MELODY needs a note and a length, like (\"C4\", 1)."
                f"\nThis one is: {entry!r}\n"
            )
        name, beats = entry
        if beats <= 0:
            raise SystemExit(
                f"\nThe note {name!r} lasts {beats} beats. It has to be more than 0.\n"
            )
        number = note_number(name)
        if number is not None:
            numbers.append(number)

    if not numbers:
        raise SystemExit("\nMELODY is all rests — add some real notes.\n")

    return min(numbers), max(numbers)


def build_platform(index, previous, lowest, highest):
    """Work out where platform number `index` sits in the world."""
    name, beats = MELODY[index % len(MELODY)]
    number = note_number(name)

    if number is None:
        fraction = 0.5 if previous is None else previous["fraction"]
    else:
        fraction = platform_height(number, lowest, highest)
        if not isinstance(fraction, (int, float)):
            raise SystemExit(
                "\nplatform_height() has to return a number between 0 and 1."
                f"\nRight now it returns {fraction!r}.\n"
            )
        fraction = max(0.0, min(1.0, fraction))

    if previous is None:
        x = 0.0
        air = MAX_AIR
    else:
        seconds_per_beat = 60.0 / TEMPO
        air = min(previous["beats"] * seconds_per_beat, MAX_AIR)
        x = previous["x"] + GAP_PER_SECOND * air + MIN_GAP

    return {
        "index": index,
        "name": name,
        "number": number,
        "beats": beats,
        "fraction": fraction,
        "x": x,
        "y": PLAY_BOTTOM - fraction * (PLAY_BOTTOM - PLAY_TOP),
        "air": air,           # time it takes to arrive here from the one before
        "glow": 0.0,
    }


# ---------- drawing helpers ----------

def make_sky():
    sky = pygame.Surface((1, HEIGHT))
    for y in range(HEIGHT):
        blend = y / (HEIGHT - 1)
        sky.set_at((0, y), tuple(
            int(SKY_TOP[c] + (SKY_BOTTOM[c] - SKY_TOP[c]) * blend) for c in range(3)
        ))
    return pygame.transform.scale(sky, (WIDTH, HEIGHT))


def make_glow(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    for r in range(radius, 0, -1):
        alpha = int(70 * (1 - r / radius) ** 2)
        pygame.draw.circle(surf, (*color, alpha), (radius, radius), r)
    return surf


def blit_centered(screen, surf, x, y):
    screen.blit(surf, (x - surf.get_width() / 2, y - surf.get_height() / 2))


def main():
    if TEMPO <= 0:
        raise SystemExit("\nTEMPO has to be more than 0.\n")
    if VOICE not in tones.VOICES:
        raise SystemExit(
            f"\nThere's no voice called {VOICE!r}."
            f"\nPick one of: {', '.join(sorted(tones.VOICES))}\n"
        )
    lowest, highest = check_melody()

    tones.init_mixer()
    pygame.init()
    pygame.display.set_caption(f"Melody Jumper — {SONG_TITLE}")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 22)
    big_font = pygame.font.Font(None, 30)

    # One sound per pitch used in the song, built once up front.
    wanted = []
    for name, _ in MELODY:
        number = note_number(name)
        if number is not None and number not in wanted:
            wanted.append(number)

    # A tone much longer than the gap between notes just piles up on the next
    # one, and enough of those stacked together crackle. Fit it to the song.
    longest = max(beats for _, beats in MELODY)
    tone_seconds = min(1.6, longest * (60.0 / TEMPO) + 0.5)

    sounds = {}
    for done, number in enumerate(wanted):
        screen.fill(SKY_TOP)
        msg = big_font.render("building the sounds...", True, (226, 228, 250))
        screen.blit(msg, ((WIDTH - msg.get_width()) // 2, 270))
        track = pygame.Rect(WIDTH // 2 - 180, 320, 360, 10)
        pygame.draw.rect(screen, (40, 38, 66), track, border_radius=5)
        filled = track.copy()
        filled.width = int(360 * done / max(len(wanted), 1))
        pygame.draw.rect(screen, BALL_COLOR, filled, border_radius=5)
        pygame.display.flip()
        for event in pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit()
        sounds[number] = tones.make_tone(
            tones.frequency(number), tone_seconds, VOICE)

    sky = make_sky()
    ball_glow = make_glow(58, BALL_COLOR)
    hit_glow = make_glow(70, ACTIVE_COLOR)

    # A dim line dropping away below each platform, like a music box comb.
    posts = {}
    for shade in (PLATFORM_COLOR, REST_COLOR):
        post = pygame.Surface((2, HEIGHT), pygame.SRCALPHA)
        post.fill((*shade, 26))
        posts[shade] = post

    dust = [
        [random.uniform(0, WIDTH), random.uniform(0, HEIGHT),
         random.uniform(0.10, 0.45), random.uniform(1.0, 2.2)]
        for _ in range(90)
    ]

    def extend(platforms, until_x):
        # Platform numbers keep counting up even after old ones are thrown
        # away, so the song never loses its place.
        while platforms[-1]["x"] < until_x:
            platforms.append(build_platform(
                platforms[-1]["index"] + 1, platforms[-1], lowest, highest))

    def start():
        platforms = [build_platform(0, None, lowest, highest)]
        extend(platforms, WIDTH * 2)
        first = platforms[0]
        if first["number"] is not None:
            sounds[first["number"]].play()
            first["glow"] = 1.0
        return platforms

    platforms = start()
    current = 0                  # which platform the ball is on or leaving
    flying = False
    timer = 0.0                  # seconds spent sitting, or seconds into the jump
    ball_x, ball_y = platforms[0]["x"], platforms[0]["y"] - BALL_RADIUS
    start_x = start_y = launch_vy = travel_vx = 0.0
    camera = ball_x - WIDTH * CAMERA_ANCHOR
    squash = 0.0
    trail = []
    rings = []
    paused = False
    played = 1 if platforms[0]["number"] is not None else 0

    while True:
        dt = min(clock.tick(60) / 1000.0, 0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_r:
                    platforms = start()
                    current, flying, timer = 0, False, 0.0
                    played = 1 if platforms[0]["number"] is not None else 0
                    ball_x, ball_y = platforms[0]["x"], platforms[0]["y"] - BALL_RADIUS
                    camera = ball_x - WIDTH * CAMERA_ANCHOR
                    trail, rings, squash = [], [], 0.0

        if not paused:
            seconds_per_beat = 60.0 / TEMPO
            timer += dt

            if flying:
                travel = platforms[current + 1]["air"]
                ball_x = start_x + travel_vx * timer
                ball_y = start_y + launch_vy * timer + 0.5 * GRAVITY * timer * timer

                trail.append([ball_x, ball_y, 1.0])

                if timer >= travel:
                    current += 1
                    landed = platforms[current]
                    ball_x, ball_y = landed["x"], landed["y"] - BALL_RADIUS
                    flying = False
                    timer -= travel          # keep the leftover so the beat can't drift
                    squash = 1.0
                    landed["glow"] = 1.0
                    rings.append([ball_x, landed["y"], 0.0, 1.0])
                    if landed["number"] is not None:
                        sounds[landed["number"]].play()
                        played += 1
            else:
                # Sit on the platform for whatever is left of the note.
                here = platforms[current]
                dwell = max(0.0, here["beats"] * seconds_per_beat - platforms[current + 1]["air"])
                if timer >= dwell:
                    nxt = platforms[current + 1]
                    travel = nxt["air"]
                    start_x, start_y = ball_x, ball_y
                    target_y = nxt["y"] - BALL_RADIUS
                    travel_vx = (nxt["x"] - start_x) / travel
                    launch_vy = ((target_y - start_y) - 0.5 * GRAVITY * travel * travel) / travel
                    flying = True
                    timer -= dwell

            # Keep enough level ahead of the ball, and throw away what's behind.
            extend(platforms, ball_x + WIDTH * 1.5)
            while platforms[0]["x"] < camera - WIDTH * 0.5 and current > 2:
                platforms.pop(0)
                current -= 1

            camera += (ball_x - WIDTH * CAMERA_ANCHOR - camera) * min(1.0, 6.0 * dt)
            squash = max(0.0, squash - dt * 4.5)

            for p in platforms:
                p["glow"] = max(0.0, p["glow"] - dt * 2.2)
            for ring in rings:
                ring[2] += dt * 150
                ring[3] -= dt * 2.4
            rings = [r for r in rings if r[3] > 0]
            for spot in trail:
                spot[2] -= dt * 3.2
            trail = [s for s in trail if s[2] > 0][-18:]

            for d in dust:
                d[0] -= d[2] * 14 * dt

        # ---------- draw ----------
        screen.blit(sky, (0, 0))

        for d in dust:
            sx = (d[0] - camera * d[2]) % (WIDTH + 40) - 20
            shade = int(40 + 70 * d[2])
            pygame.draw.circle(screen, (shade, shade, shade + 20), (int(sx), int(d[1])), int(d[3]))

        for p in platforms:
            sx = p["x"] - camera
            if sx < -PLATFORM_WIDTH or sx > WIDTH + PLATFORM_WIDTH:
                continue

            is_rest = p["number"] is None
            base = REST_COLOR if is_rest else PLATFORM_COLOR
            color = tuple(int(base[c] + (ACTIVE_COLOR[c] - base[c]) * p["glow"]) for c in range(3))

            screen.blit(posts[base], (sx - 1, p["y"]))

            if p["glow"] > 0.01:
                glow = hit_glow.copy()
                glow.set_alpha(int(255 * p["glow"]))
                blit_centered(screen, glow, sx, p["y"])

            rect = pygame.Rect(0, 0, PLATFORM_WIDTH, PLATFORM_HEIGHT)
            rect.center = (sx, p["y"] + PLATFORM_HEIGHT / 2)
            if is_rest:
                pygame.draw.rect(screen, color, rect, width=2, border_radius=6)
            else:
                pygame.draw.rect(screen, color, rect, border_radius=6)

            label = font.render(p["name"], True, color if p["glow"] > 0.3 else TEXT_COLOR)
            screen.blit(label, (sx - label.get_width() / 2, p["y"] + 22))

        for x, y, radius, life in rings:
            ring = pygame.Surface((int(radius) * 2 + 8, int(radius) * 2 + 8), pygame.SRCALPHA)
            pygame.draw.circle(ring, (*ACTIVE_COLOR, int(150 * life)),
                               (ring.get_width() // 2, ring.get_height() // 2),
                               int(radius), width=3)
            blit_centered(screen, ring, x - camera, y)

        for tx, ty, life in trail:
            dot = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2), pygame.SRCALPHA)
            pygame.draw.circle(dot, (*BALL_COLOR, int(70 * life)),
                               (BALL_RADIUS, BALL_RADIUS), max(1, int(BALL_RADIUS * life * 0.8)))
            blit_centered(screen, dot, tx - camera, ty)

        blit_centered(screen, ball_glow, ball_x - camera, ball_y)
        wide = BALL_RADIUS * (1 + 0.45 * squash)
        tall = BALL_RADIUS * (1 - 0.40 * squash)
        pygame.draw.ellipse(screen, BALL_COLOR, pygame.Rect(
            ball_x - camera - wide, ball_y - tall, wide * 2, tall * 2))

        screen.blit(big_font.render(SONG_TITLE, True, (226, 228, 250)), (24, 22))
        counted = f"{played} note{'' if played == 1 else 's'} played"
        screen.blit(font.render(f"{TEMPO} bpm    {VOICE}    {counted}",
                                True, TEXT_COLOR), (25, 52))
        hint = "SPACE paused — press it again" if paused else "SPACE pause    R restart    ESC quit"
        screen.blit(font.render(hint, True, TEXT_COLOR), (25, HEIGHT - 34))

        pygame.display.flip()


if __name__ == "__main__":
    main()
