"""
Note Finder — work out a song by ear, one note at a time.

Your computer keyboard becomes a piano. Hunt around until a note matches the
song in your head. Nothing is written down while you hunt — wrong guesses cost
you nothing. When you find the right one, press ENTER to keep it.

Everything you keep is saved straight into my_song.py, and jumper.py plays it
the next time you run it.

Run it from the python-games folder:

    ./venv/bin/python melody-jumper/finder.py

  a w s e d f t g y h u j k o l p ;   the piano — hold a key for as long as
                                      the note lasts, then let go
  ENTER                               keep the note you just played
  SPACE                               hold it for a silence, then ENTER
  BACKSPACE                           throw away the last note you kept
  Z / X                               move down / up an octave
  Q                                   hold a low drone to compare against
  TAB                                 play back what you've kept
  ESC                                 quit
"""

import os
import sys

import pygame

import tones


# ============================================================
#  YOUR CODE — everything you change lives up here
# ============================================================

SONG_TITLE = "My Song"

# Beats per minute. Set this to roughly the speed of the song you're working
# out BEFORE you start, because it decides how your held notes get measured.
TEMPO = 92

# Which octave the 'a' key plays. 4 is the octave around middle C.
START_OCTAVE = 4

# How the notes sound while you hunt. One of:
# bell, pluck, lead, heavy, searing, moog, solo
VOICE = "pluck"

# The note Q holds underneath everything. Pick the note your song feels like
# it "comes home" to, and every other note becomes easier to judge.
DRONE_NOTE = "C3"


def on_note_played(note_name, held_beats):
    """
    Runs when you press ENTER to keep a note.

    `note_name` is what you played, like "D4" or "-" for a silence.
    `held_beats` is how long you held it, rounded to the nearest half beat.

    Return the pair that should go into your song — or return None to keep
    nothing at all.
    """
    return (note_name, held_beats)

    # YOUR TURN — try each of these instead of the line above.
    #   return (note_name, 1)                  (every note the same length)
    #   return None                            (why does nothing get kept?)
    #   return (note_name, held_beats * 2)     (a song at half speed)
    #
    #   if held_beats < 1:                     (ignore quick taps entirely)
    #       return None
    #   return (note_name, held_beats)


KEY_COLOR = (238, 240, 250)
PRESSED_COLOR = (255, 208, 96)
ACCENT = (255, 208, 96)


# ============================================================
#  THE MACHINERY — you don't have to read this yet
# ============================================================

WIDTH, HEIGHT = 960, 620
SAVE_AS = "my_song.py"

BACKGROUND = (16, 15, 32)
PANEL = (26, 24, 48)
TEXT = (150, 152, 190)
BRIGHT = (226, 228, 250)
DIM = (108, 110, 145)
BLACK_KEY = (28, 27, 44)
REST_COLOR = (110, 112, 150)

# Where each computer key sits on a piano, counting in semitones from the left.
# This is the layout GarageBand and Ableton use. R and I are deliberately not
# on it — there's no black key between E and F, or between B and C.
KEY_ORDER = "awsedftgyhujkolp;"
BLACK_KEYS = {1, 3, 6, 8, 10, 13, 15}

WHITE_W, WHITE_H = 64, 178
BLACK_W, BLACK_H = 40, 110
PIANO_Y = 400

SNAP_TO = 0.5             # round held notes to the nearest half beat
MIN_BEATS, MAX_BEATS = 0.5, 4.0
TONE_SECONDS = 0.9


def white_count(upto):
    return sum(1 for i in range(upto) if i not in BLACK_KEYS)


TOTAL_WHITE = white_count(len(KEY_ORDER))
PIANO_X = (WIDTH - TOTAL_WHITE * WHITE_W) // 2


def key_rect(step):
    """Where the piano key for this semitone is drawn."""
    if step in BLACK_KEYS:
        left = PIANO_X + white_count(step) * WHITE_W - BLACK_W // 2
        return pygame.Rect(left, PIANO_Y, BLACK_W, BLACK_H)
    return pygame.Rect(PIANO_X + white_count(step) * WHITE_W, PIANO_Y, WHITE_W, WHITE_H)


def tidy(beats):
    """1.0 shows as '1', 1.5 stays '1.5'."""
    return str(int(beats)) if float(beats) == int(beats) else f"{beats:g}"


def quantize(seconds_held, seconds_per_beat):
    """How many beats was that? Rounded to something tidy."""
    beats = seconds_held / seconds_per_beat
    beats = round(beats / SNAP_TO) * SNAP_TO
    return max(MIN_BEATS, min(MAX_BEATS, beats))


def as_python(melody):
    """The song, written the way you'd type it into jumper.py."""
    lines = ["MELODY = ["]
    lines += [f'    ({name!r}, {tidy(beats)}),' for name, beats in melody]
    lines.append("]")
    return lines


def save(melody, path):
    text = [
        "# Written by finder.py. Run jumper.py and it plays this.",
        "# It's just a list — you can edit it by hand too.",
        "",
        f"SONG_TITLE = {SONG_TITLE!r}",
        f"TEMPO = {TEMPO}",
        "",
    ] + as_python(melody) + [""]
    with open(path, "w") as handle:
        handle.write("\n".join(text))


def mono_font(size):
    """A font where every letter is the same width, so code lines up."""
    try:
        found = pygame.font.match_font("menlo,dejavusansmono,couriernew,monaco,consolas")
        if found:
            return pygame.font.Font(found, size)
    except Exception:
        pass
    return pygame.font.Font(None, size + 2)


def main():
    if TEMPO <= 0:
        raise SystemExit("\nTEMPO has to be more than 0.\n")
    if VOICE not in tones.VOICES:
        raise SystemExit(
            f"\nThere's no voice called {VOICE!r}."
            f"\nPick one of: {', '.join(sorted(tones.VOICES))}\n"
        )
    try:
        drone_number = tones.note_number(DRONE_NOTE)
    except ValueError as problem:
        raise SystemExit(f"\nDRONE_NOTE: {problem}\n")

    tones.init_mixer()
    pygame.init()
    pygame.mixer.set_num_channels(24)
    pygame.display.set_caption("Note Finder")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 22)
    small = pygame.font.Font(None, 19)
    big = pygame.font.Font(None, 30)
    code = mono_font(17)

    keymap = {pygame.key.key_code(ch): i for i, ch in enumerate(KEY_ORDER)}
    labels = {i: ch.upper() for i, ch in enumerate(KEY_ORDER)}
    save_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), SAVE_AS)

    octave = START_OCTAVE
    cache = {}

    def tone_for(number):
        if number not in cache:
            cache[number] = tones.make_tone(
                tones.frequency(number), TONE_SECONDS, VOICE)
        return cache[number]

    def build_octave():
        """Get every note on screen ready, so pressing a key is instant."""
        base = (octave + 1) * 12
        missing = [base + s for s in range(len(KEY_ORDER)) if base + s not in cache]
        for done, number in enumerate(missing):
            screen.fill(BACKGROUND)
            msg = big.render("building the sounds...", True, BRIGHT)
            screen.blit(msg, ((WIDTH - msg.get_width()) // 2, 270))
            bar = pygame.Rect(WIDTH // 2 - 180, 320, 360, 10)
            pygame.draw.rect(screen, PANEL, bar, border_radius=5)
            filled = bar.copy()
            filled.width = int(360 * done / max(len(missing), 1))
            pygame.draw.rect(screen, ACCENT, filled, border_radius=5)
            pygame.display.flip()
            for event in pygame.event.get(pygame.QUIT):
                pygame.quit()
                sys.exit()
            tone_for(number)
        return base

    base = build_octave()

    recorded = []             # the notes you've decided to keep
    last_played = None        # the one note you just tried, not kept yet
    held = {}                 # step -> (when it went down, channel, key)
    rest_from = None
    drone = None
    playing = None
    play_at = 0
    status = "Hunt for a note. Nothing is written down until you press ENTER."

    def leave():
        """On the way out, print the song so it can be pasted anywhere."""
        pygame.quit()
        if recorded:
            print(f"\nYour song, saved to {SAVE_AS}. You can also paste this straight")
            print("into jumper.py:\n")
            print("\n".join(as_python(recorded)))
            print()
        sys.exit()

    while True:
        clock.tick(60)
        now = pygame.time.get_ticks() / 1000.0
        spb = 60.0 / TEMPO

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                leave()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    leave()

                elif event.key in keymap:
                    step = keymap[event.key]
                    if step not in held:
                        held[step] = (now, tone_for(base + step).play(), event.key)

                elif event.key == pygame.K_SPACE and rest_from is None:
                    rest_from = now

                elif event.key == pygame.K_RETURN:
                    if last_played is None:
                        status = "Play a note first, then press ENTER to keep it."
                    else:
                        name, beats = last_played
                        kept = on_note_played(name, beats)
                        if kept is None:
                            status = f"on_note_played() returned None — {name} not kept"
                        elif (not isinstance(kept, (tuple, list)) or len(kept) != 2):
                            raise SystemExit(
                                "\non_note_played() has to return a pair like"
                                ' ("D4", 1.5), or None.'
                                f"\nRight now it returns {kept!r}.\n"
                            )
                        else:
                            keep_name, keep_beats = kept
                            try:
                                float(keep_beats)
                            except (TypeError, ValueError):
                                raise SystemExit(
                                    "\non_note_played() returned a length that isn't a"
                                    f" number: {keep_beats!r}\n"
                                )
                            if float(keep_beats) <= 0:
                                raise SystemExit(
                                    f"\non_note_played() returned a length of"
                                    f" {keep_beats}. It has to be more than 0.\n"
                                )
                            recorded.append((keep_name, float(keep_beats)))
                            save(recorded, save_path)
                            plural = "" if len(recorded) == 1 else "s"
                            status = (f"kept {keep_name} — "
                                      f"{len(recorded)} note{plural} so far")
                        last_played = None

                elif event.key == pygame.K_BACKSPACE and recorded:
                    gone = recorded.pop()
                    save(recorded, save_path)
                    status = f"threw away {gone[0]}"

                elif event.key in (pygame.K_z, pygame.K_x,
                                   pygame.K_DOWN, pygame.K_UP) and not held:
                    up = event.key in (pygame.K_x, pygame.K_UP)
                    octave = min(7, octave + 1) if up else max(1, octave - 1)
                    base = build_octave()
                    status = f"octave {octave} — 'a' is now {tones.note_name(base)}"

                elif event.key == pygame.K_q:
                    if drone is None:
                        drone = tone_for(drone_number).play(loops=-1)
                        status = f"drone on — holding {DRONE_NOTE} underneath"
                    else:
                        drone.fadeout(200)
                        drone = None
                        status = "drone off"

                elif event.key == pygame.K_TAB and recorded:
                    playing = 0
                    play_at = now
                    status = "playing back what you've kept"

            elif event.type == pygame.KEYUP:
                for step in [s for s, (_, _, k) in held.items() if k == event.key]:
                    started, channel, _ = held.pop(step)
                    if channel:
                        channel.fadeout(140)
                    name = tones.note_name(base + step)
                    last_played = (name, quantize(now - started, spb))
                    status = f"{name} for {tidy(last_played[1])} beats — ENTER to keep it"

                if event.key == pygame.K_SPACE and rest_from is not None:
                    last_played = ("-", quantize(now - rest_from, spb))
                    rest_from = None
                    status = f"a silence, {tidy(last_played[1])} beats — ENTER to keep it"

        if playing is not None:
            if playing >= len(recorded):
                playing = None
                status = "that's what you have so far"
            elif now >= play_at:
                name, beats = recorded[playing]
                if name != "-":
                    try:
                        tone_for(tones.note_number(name)).play()
                    except ValueError:
                        pass
                play_at = now + beats * spb
                playing += 1

        # ---------- draw ----------
        screen.fill(BACKGROUND)

        screen.blit(big.render(SONG_TITLE, True, BRIGHT), (28, 22))
        head = (f"{TEMPO} bpm    octave {octave}    voice: {VOICE}"
                f"    {len(recorded)} kept" + ("    drone on" if drone else ""))
        screen.blit(font.render(head, True, TEXT), (29, 54))

        # The song so far, written exactly the way jumper.py wants it.
        panel = pygame.Rect(24, 84, 470, 300)
        pygame.draw.rect(screen, PANEL, panel, border_radius=10)
        lines = as_python(recorded)
        fits = (panel.height - 24) // 20
        if len(lines) > fits:                       # keep the newest visible
            lines = [lines[0], f"    ... {len(recorded) - (fits - 2)} more above"] \
                + lines[-(fits - 2):]
        for i, line in enumerate(lines):
            shade = DIM if line.startswith("    ...") else (
                BRIGHT if line.strip().startswith("(") else ACCENT)
            screen.blit(code.render(line, True, shade), (panel.x + 16, panel.y + 14 + i * 20))

        # The one note you're holding, or just played, waiting to be kept.
        stage = pygame.Rect(514, 84, WIDTH - 538, 300)
        pygame.draw.rect(screen, PANEL, stage, border_radius=10)
        if held or rest_from is not None:
            started = min([t for t, _, _ in held.values()] +
                          ([rest_from] if rest_from is not None else []))
            raw = (now - started) / spb
            snapped = quantize(now - started, spb)
            screen.blit(small.render("holding", True, TEXT), (stage.x + 20, stage.y + 22))
            screen.blit(big.render(f"{raw:.2f} beats", True, TEXT),
                        (stage.x + 20, stage.y + 46))
            screen.blit(small.render("which rounds to", True, TEXT),
                        (stage.x + 20, stage.y + 88))
            screen.blit(big.render(f"{tidy(snapped)}", True, ACCENT),
                        (stage.x + 20, stage.y + 112))
        elif last_played is not None:
            screen.blit(small.render("ready to keep", True, TEXT),
                        (stage.x + 20, stage.y + 22))
            shown = f'("{last_played[0]}", {tidy(last_played[1])})'
            screen.blit(code.render(shown, True, ACCENT), (stage.x + 20, stage.y + 52))
            screen.blit(small.render("ENTER keeps it.", True, BRIGHT),
                        (stage.x + 20, stage.y + 84))
            screen.blit(small.render("Or just play another note —", True, TEXT),
                        (stage.x + 20, stage.y + 106))
            screen.blit(small.render("this one costs you nothing.", True, TEXT),
                        (stage.x + 20, stage.y + 126))
        else:
            for i, line in enumerate([
                    "Hold a key to hear a note.",
                    "",
                    "Nothing is written down while",
                    "you hunt. Wrong guesses are",
                    "free — that's the point.",
                    "",
                    "When one matches the song in",
                    "your head, press ENTER."]):
                screen.blit(small.render(line, True, TEXT),
                            (stage.x + 20, stage.y + 24 + i * 22))

        msg = small.render(status, True, TEXT)
        screen.blit(msg, ((WIDTH - msg.get_width()) // 2, PIANO_Y - 26))

        for step in range(len(KEY_ORDER)):
            if step in BLACK_KEYS:
                continue
            rect = key_rect(step)
            down = step in held
            pygame.draw.rect(screen, PRESSED_COLOR if down else KEY_COLOR, rect,
                             border_radius=6)
            pygame.draw.rect(screen, BACKGROUND, rect, width=2, border_radius=6)
            label = small.render(labels[step], True, (60, 60, 80))
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.bottom - 32))
            nm = small.render(tones.note_name(base + step), True, (140, 140, 165))
            screen.blit(nm, (rect.centerx - nm.get_width() // 2, rect.bottom - 54))

        for step in sorted(BLACK_KEYS):
            if step >= len(KEY_ORDER):
                continue
            rect = key_rect(step)
            down = step in held
            pygame.draw.rect(screen, PRESSED_COLOR if down else BLACK_KEY, rect,
                             border_radius=5)
            label = small.render(labels[step], True,
                                 (60, 60, 80) if down else (170, 172, 200))
            screen.blit(label, (rect.centerx - label.get_width() // 2, rect.bottom - 24))

        footer = ("ENTER keep    SPACE silence    BACKSPACE undo    "
                  "Z/X octave    Q drone    TAB play back    ESC quit")
        screen.blit(small.render(footer, True, TEXT), (28, HEIGHT - 26))

        pygame.display.flip()


if __name__ == "__main__":
    main()
