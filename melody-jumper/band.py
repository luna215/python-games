"""
Band — three instruments, three balls, one clock.

Lesson 1 had one ball playing one tune. This has a ball per instrument, and
they all have to stay together. That turns out to change how the whole thing is
built.

In jumper.py, a platform's position came from the note before it. That works
fine for one ball and falls apart for three: a part playing eight short notes
would run twice as far along the screen as a part playing four long ones, and
the balls would drift apart within seconds.

So here, position comes from *time*. A note that starts on beat 12 is drawn at
beat 12, whatever else is going on. Everything lines up because everything is
measured against the same clock — which is exactly how a real band works.

Run it from the python-games folder:

    ./venv/bin/python melody-jumper/band.py

SPACE pauses.  R starts over.  Number keys mute an instrument.  ESC quits.
"""

import math
import sys

import pygame

import tones


# ============================================================
#  YOUR CODE — everything you change lives up here
# ============================================================

SONG_TITLE = "In the Hall of the Mountain King"

# 138 is the speed written on Grieg's score. The real piece gets faster and
# faster all the way to the end — turn this up to 220 and you'll recognise it.
TEMPO = 138
BEATS_PER_BAR = 4

# What the harmony does under each bar. Only drawn on screen, but it's real:
# the bass sits on B for three bars and moves to D for the fourth.
CHORDS = ["Bm", "Bm", "Bm", "D"]

# One entry per instrument, top of the screen to bottom.
#
# The top three all play THE SAME four-bar tune, an octave apart each time.
# That's not a shortcut — it's what the piece actually does. Grieg starts it
# low and quiet on cellos, basses and bassoons, then hands it up the orchestra,
# adding players until everyone is playing at once. is_playing() below is what
# makes that happen here.
PARTS = [
    {
        "name": "high",
        "voice": "solo",
        "color": (255, 208, 96),
        "melody": [
            ("B4", 0.5), ("C#5", 0.5), ("D5", 0.5), ("E5", 0.5), ("F#5", 0.5), ("D5", 0.5), ("F#5", 1),
            ("F5", 0.5), ("C#5", 0.5), ("F5", 1),   ("E5", 0.5), ("C5", 0.5),  ("E5", 1),
            ("B4", 0.5), ("C#5", 0.5), ("D5", 0.5), ("E5", 0.5), ("F#5", 0.5), ("D5", 0.5), ("F#5", 0.5), ("B5", 0.5),
            ("A5", 0.5), ("F#5", 0.5), ("D5", 0.5), ("F#5", 0.5), ("A5", 1),   ("-",  1),
        ],
    },
    {
        "name": "mid",
        "voice": "pluck",
        "color": (129, 196, 255),
        "melody": [
            ("B3", 0.5), ("C#4", 0.5), ("D4", 0.5), ("E4", 0.5), ("F#4", 0.5), ("D4", 0.5), ("F#4", 1),
            ("F4", 0.5), ("C#4", 0.5), ("F4", 1),   ("E4", 0.5), ("C4", 0.5),  ("E4", 1),
            ("B3", 0.5), ("C#4", 0.5), ("D4", 0.5), ("E4", 0.5), ("F#4", 0.5), ("D4", 0.5), ("F#4", 0.5), ("B4", 0.5),
            ("A4", 0.5), ("F#4", 0.5), ("D4", 0.5), ("F#4", 0.5), ("A4", 1),   ("-",  1),
        ],
    },
    {
        "name": "low",
        "voice": "heavy",
        "color": (176, 138, 255),
        # Where the cellos, double basses and bassoons actually play it.
        "melody": [
            ("B2", 0.5), ("C#3", 0.5), ("D3", 0.5), ("E3", 0.5), ("F#3", 0.5), ("D3", 0.5), ("F#3", 1),
            ("F3", 0.5), ("C#3", 0.5), ("F3", 1),   ("E3", 0.5), ("C3", 0.5),  ("E3", 1),
            ("B2", 0.5), ("C#3", 0.5), ("D3", 0.5), ("E3", 0.5), ("F#3", 0.5), ("D3", 0.5), ("F#3", 0.5), ("B3", 0.5),
            ("A3", 0.5), ("F#3", 0.5), ("D3", 0.5), ("F#3", 0.5), ("A3", 1),   ("-",  1),
        ],
    },
    {
        "name": "pulse",
        "voice": "bell",
        "color": (120, 230, 180),
        # The left hand of Grieg's own piano version: rocking between the home
        # note and the one five steps above it, then moving up for the last bar.
        "melody": [
            ("B2", 1), ("F#2", 1), ("B2", 1), ("F#2", 1),
            ("B2", 1), ("F#2", 1), ("B2", 1), ("F#2", 1),
            ("B2", 1), ("F#2", 1), ("B2", 1), ("F#2", 1),
            ("D3", 1), ("A2", 1),  ("D3", 1), ("A2", 1),
        ],
    },
]


def is_playing(part_name, bar_number):
    """
    Runs at the start of every bar, for every instrument.

    Return True if that instrument should play this bar, or False to rest it.
    The ball keeps hopping either way — it just goes quiet, and its platforms
    turn hollow so you can still see what it would have played.

    Bars are counted from 0. The tune is 4 bars long, so a new instrument
    joining every 4 bars means one more each time the tune comes round.
    """
    if part_name == "low":
        return True                     # starts alone, quiet and low
    if part_name == "pulse":
        return bar_number >= 4          # joins on the second time through
    if part_name == "mid":
        return bar_number >= 8
    if part_name == "high":
        return bar_number >= 12         # the screaming one arrives last
    return True

    # YOUR TURN — try each of these instead of everything above.
    #   return True                             (everyone in from the start —
    #                                            listen to how much worse it is)
    #
    #   return part_name != "high"              (drop the top line entirely)
    #
    #   if part_name == "pulse":                (pulse on alternate bars only)
    #       return bar_number % 2 == 0
    #   return True
    #
    #   return bar_number % 8 < 6               (everything drops for two bars)


# ============================================================
#  THE MACHINERY — you don't have to read this yet
# ============================================================

WIDTH, HEIGHT = 1000, 700
LANES_TOP, LANES_BOTTOM = 132, 632
PLAYHEAD = 0.32                # where "now" sits across the screen
PIXELS_PER_BEAT = 110

GUTTER_W = 104
PAD_HEIGHT = 12
PAD_INSET = 5                  # so touching notes still look like separate pads
LANE_PADDING = 26
BALL_RADIUS = 11
HOP_SECONDS = 0.26
ARC_HEIGHT = 30

BACKGROUND = (13, 12, 28)
LANE_SHADE = (21, 20, 42)
GRID = (38, 36, 66)
BAR_LINE = (58, 54, 96)
TEXT = (150, 152, 190)
BRIGHT = (226, 228, 250)
DIM = (92, 94, 128)


def prepare(part):
    """Work out when each note starts, and how high each one sits."""
    melody = part["melody"]
    if len(melody) < 1:
        raise SystemExit(f"\nThe part {part['name']!r} has no notes in it.\n")

    starts, running = [], 0.0
    numbers = []
    for entry in melody:
        if not isinstance(entry, (tuple, list)) or len(entry) != 2:
            raise SystemExit(
                f"\nEvery note in {part['name']!r} needs a name and a length,"
                f' like ("C4", 1).\nThis one is: {entry!r}\n'
            )
        name, beats = entry
        if beats <= 0:
            raise SystemExit(
                f"\nIn {part['name']!r}, the note {name!r} lasts {beats} beats."
                "\nIt has to be more than 0.\n"
            )
        try:
            number = tones.note_number(name)
        except ValueError as problem:
            raise SystemExit(f"\nIn the part {part['name']!r}: {problem}\n")
        numbers.append(number)
        starts.append(running)
        running += beats

    real = [n for n in numbers if n is not None]
    if not real:
        raise SystemExit(f"\nThe part {part['name']!r} is nothing but rests.\n")

    part["starts"] = starts
    part["numbers"] = numbers
    part["total"] = running
    part["low"], part["high"] = min(real), max(real)
    part["longest"] = max(b for _, b in melody)
    return part


def note_at(part, beat):
    """Which note is sounding at this moment, and when did it start?"""
    cycle, within = divmod(beat, part["total"])
    starts = part["starts"]
    index = 0
    for i in range(len(starts) - 1, -1, -1):
        if within >= starts[i] - 1e-9:
            index = i
            break
    count = len(part["melody"])
    return int(cycle) * count + index, cycle * part["total"] + starts[index]


def note_by_index(part, index):
    """The name, length and start beat of note number `index`, counting forever."""
    count = len(part["melody"])
    cycle, i = divmod(index, count)
    name, beats = part["melody"][i]
    return name, beats, cycle * part["total"] + part["starts"][i], part["numbers"][i]


def lane_of(part_index, count):
    height = (LANES_BOTTOM - LANES_TOP) / count
    return LANES_TOP + part_index * height, height


def pad_y(part, number, part_index, count):
    """How high up its own lane a note sits."""
    top, height = lane_of(part_index, count)
    # With a lot of instruments the lanes get thin, so the padding has to give
    # way — otherwise there is no room left and the pitches come out upside down.
    padding = min(LANE_PADDING, max(3.0, height * 0.16))
    inner = max(0.0, height - 2 * padding - PAD_HEIGHT)
    span = part["high"] - part["low"]
    fraction = 0.5 if span == 0 else (number - part["low"]) / span
    return top + padding + (1 - fraction) * inner


def main():
    if TEMPO <= 0:
        raise SystemExit("\nTEMPO has to be more than 0.\n")
    if BEATS_PER_BAR <= 0:
        raise SystemExit("\nBEATS_PER_BAR has to be more than 0.\n")
    if not PARTS:
        raise SystemExit("\nPARTS is empty — add at least one instrument.\n")

    for part in PARTS:
        for field in ("name", "voice", "color", "melody"):
            if field not in part:
                raise SystemExit(
                    f"\nOne of the PARTS is missing its {field!r}."
                    f"\nEvery part needs a name, a voice, a color and a melody.\n"
                )
        if part["voice"] not in tones.VOICES:
            raise SystemExit(
                f"\nThe part {part['name']!r} asks for a voice called"
                f" {part['voice']!r}, which doesn't exist."
                f"\nPick one of: {', '.join(sorted(tones.VOICES))}\n"
            )
        prepare(part)

    tones.init_mixer()
    pygame.init()
    pygame.mixer.set_num_channels(32)
    pygame.display.set_caption(f"Band — {SONG_TITLE}")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 22)
    small = pygame.font.Font(None, 19)
    big = pygame.font.Font(None, 32)

    spb = 60.0 / TEMPO

    # One sound per pitch per voice. A note played by the bass and by the lead
    # is the same pitch but a different sound, so it gets built twice.
    wanted, seen = [], set()
    for part in PARTS:
        length = min(2.4, part["longest"] * spb + 0.5)
        for number in part["numbers"]:
            key = (part["voice"], number)
            if number is not None and key not in seen:
                seen.add(key)
                wanted.append((key, length))

    sounds = {}
    for done, ((voice, number), length) in enumerate(wanted):
        screen.fill(BACKGROUND)
        msg = big.render("building the sounds...", True, BRIGHT)
        screen.blit(msg, ((WIDTH - msg.get_width()) // 2, 310))
        track = pygame.Rect(WIDTH // 2 - 180, 362, 360, 10)
        pygame.draw.rect(screen, LANE_SHADE, track, border_radius=5)
        filled = track.copy()
        filled.width = int(360 * done / max(len(wanted), 1))
        pygame.draw.rect(screen, (255, 208, 96), filled, border_radius=5)
        pygame.display.flip()
        for event in pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit()
        sounds[(voice, number)] = tones.make_tone(
            tones.frequency(number), length, voice)

    # Several instruments at full volume add up to more than the speaker can
    # take, and the result is a nasty crackle. Each one gets turned down to
    # leave room for the others.
    share = min(1.0, 1.25 / len(PARTS))
    for sound in sounds.values():
        sound.set_volume(share)

    count = len(PARTS)
    elapsed = 0.0
    paused = False
    muted = [False] * count
    sounded = [None] * count       # the last note index each part played
    flashes = {}                   # (part, note index) -> how bright, 0..1

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
                    elapsed = 0.0
                    sounded = [None] * count
                    flashes.clear()
                for slot in range(min(count, 9)):
                    if event.key == getattr(pygame, f"K_{slot + 1}"):
                        muted[slot] = not muted[slot]

        if not paused:
            elapsed += dt
        beat = elapsed / spb
        bar = int(beat // BEATS_PER_BAR)

        for key in list(flashes):
            flashes[key] -= dt * 2.4
            if flashes[key] <= 0:
                del flashes[key]

        # ---------- sound ----------
        if not paused:
            for p, part in enumerate(PARTS):
                index, _ = note_at(part, beat)
                if sounded[p] == index:
                    continue
                sounded[p] = index
                name, _, start, number = note_by_index(part, index)
                allowed = is_playing(part["name"], int(start // BEATS_PER_BAR))
                if not isinstance(allowed, bool):
                    raise SystemExit(
                        "\nis_playing() has to return True or False."
                        f"\nRight now it returns {allowed!r}.\n"
                    )
                if number is not None and allowed and not muted[p]:
                    sounds[(part["voice"], number)].play()
                    flashes[(p, index)] = 1.0

        # ---------- draw ----------
        screen.fill(BACKGROUND)
        camera = beat * PIXELS_PER_BEAT - WIDTH * PLAYHEAD
        first_beat = camera / PIXELS_PER_BEAT
        last_beat = (camera + WIDTH) / PIXELS_PER_BEAT

        for p, part in enumerate(PARTS):
            top, height = lane_of(p, count)
            if p % 2 == 0:
                pygame.draw.rect(screen, LANE_SHADE,
                                 pygame.Rect(0, int(top), WIDTH, int(height)))

        # bar lines and chord names
        for b in range(int(first_beat // BEATS_PER_BAR),
                       int(last_beat // BEATS_PER_BAR) + 2):
            x = b * BEATS_PER_BAR * PIXELS_PER_BEAT - camera
            if -80 < x < WIDTH + 80:
                pygame.draw.line(screen, BAR_LINE, (x, LANES_TOP - 26),
                                 (x, LANES_BOTTOM), 1)
                if CHORDS:
                    label = big.render(CHORDS[b % len(CHORDS)], True, GRID)
                    screen.blit(label, (x + 9, LANES_TOP - 40))
        for b in range(int(first_beat), int(last_beat) + 2):
            if b % BEATS_PER_BAR:
                x = b * PIXELS_PER_BEAT - camera
                pygame.draw.line(screen, GRID, (x, LANES_TOP), (x, LANES_BOTTOM), 1)

        for p, part in enumerate(PARTS):
            colour = part["color"]
            lane_top, lane_height = lane_of(p, count)
            middle = lane_top + lane_height / 2
            here, _ = note_at(part, beat)

            # every note with any part of itself on screen
            span = max(1, int((last_beat - first_beat) / max(part["total"], 0.5)) + 3)
            # one cycle back, so a long note straddling the loop point still draws
            base = (int(first_beat // part["total"]) - 1) * len(part["melody"])
            for index in range(base, base + span * len(part["melody"]) + 1):
                name, beats, start, number = note_by_index(part, index)
                if start + beats < first_beat or start > last_beat:
                    continue
                x = start * PIXELS_PER_BEAT - camera
                width = beats * PIXELS_PER_BEAT - PAD_INSET * 2
                if width < 3:
                    continue
                rest = number is None
                quiet = muted[p] or not is_playing(
                    part["name"], int(start // BEATS_PER_BAR))
                y = middle if rest else pad_y(part, number, p, count)

                glow = flashes.get((p, index), 0.0)
                if quiet or rest:
                    shade = DIM
                else:
                    shade = tuple(int(colour[c] + (255 - colour[c]) * glow)
                                  for c in range(3))
                pad = pygame.Rect(x + PAD_INSET, y, width, PAD_HEIGHT)
                if rest or quiet:
                    pygame.draw.rect(screen, shade, pad, width=2, border_radius=5)
                else:
                    pygame.draw.rect(screen, shade, pad, border_radius=5)
                if glow > 0.02 and not (rest or quiet):
                    ring = pygame.Rect(0, 0, int(90 * (1 - glow)), int(90 * (1 - glow)))
                    ring.center = (int(x + PAD_INSET), int(y + PAD_HEIGHT / 2))
                    if ring.width > 4:
                        surf = pygame.Surface((ring.width, ring.height), pygame.SRCALPHA)
                        pygame.draw.circle(surf, (*colour, int(150 * glow)),
                                           (ring.width // 2, ring.height // 2),
                                           ring.width // 2, width=2)
                        screen.blit(surf, ring.topleft)

            # the ball: rolls along its note, then hops to the next one
            name, beats, start, number = note_by_index(part, here)
            nxt_name, nxt_beats, nxt_start, nxt_number = note_by_index(part, here + 1)
            hop = min(HOP_SECONDS / spb, beats * 0.5, nxt_beats * 0.5)
            boundary = start + beats

            y_here = middle if number is None else pad_y(part, number, p, count)
            y_next = middle if nxt_number is None else pad_y(part, nxt_number, p, count)
            if beat >= boundary - hop:
                u = (beat - (boundary - hop)) / hop
                ball_y = (y_here + (y_next - y_here) * u
                          - ARC_HEIGHT * math.sin(math.pi * u))
            else:
                ball_y = y_here
            ball_x = WIDTH * PLAYHEAD

            quiet_now = muted[p] or not is_playing(
                part["name"], int(start // BEATS_PER_BAR))
            shade = DIM if quiet_now else part["color"]
            pygame.draw.circle(screen, shade,
                               (int(ball_x), int(ball_y - BALL_RADIUS)), BALL_RADIUS)

        # A solid strip down the left, so notes scrolling past don't run
        # underneath the instrument names.
        gutter = pygame.Rect(0, LANES_TOP, GUTTER_W, LANES_BOTTOM - LANES_TOP)
        pygame.draw.rect(screen, BACKGROUND, gutter)
        pygame.draw.line(screen, GRID, (GUTTER_W, LANES_TOP),
                         (GUTTER_W, LANES_BOTTOM), 1)
        for p, part in enumerate(PARTS):
            lane_top, _ = lane_of(p, count)
            off = muted[p] or not is_playing(part["name"], bar)
            screen.blit(small.render(f"{p + 1}  {part['name']}", True,
                                     DIM if off else part["color"]),
                        (14, lane_top + 10))
            screen.blit(small.render(part["voice"], True, GRID), (14, lane_top + 30))
            if off:
                screen.blit(small.render("off", True, DIM), (14, lane_top + 50))

        pygame.draw.line(screen, (70, 66, 108),
                         (WIDTH * PLAYHEAD, LANES_TOP - 26),
                         (WIDTH * PLAYHEAD, LANES_BOTTOM), 1)

        screen.blit(big.render(SONG_TITLE, True, BRIGHT), (16, 22))
        head = (f"{TEMPO} bpm    bar {bar + 1}    "
                f"{CHORDS[bar % len(CHORDS)] if CHORDS else ''}    "
                f"{len(PARTS)} instruments")
        screen.blit(font.render(head, True, TEXT), (17, 56))
        keys = " ".join(str(i + 1) for i in range(min(count, 9)))
        hint = ("SPACE paused" if paused else
                f"SPACE pause    R restart    {keys} mute    ESC quit")
        screen.blit(small.render(hint, True, TEXT), (16, HEIGHT - 26))

        pygame.display.flip()


if __name__ == "__main__":
    main()
