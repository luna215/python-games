"""
tones.py — the sound engine, shared by jumper.py and finder.py.

Both programs need to turn a note name into a sound, so that job lives here
instead of being written twice. This is what a "module" is: code you wrote once
and use from more than one place.

Nothing in here needs changing to do the lessons. If you're curious how a
computer makes a sound out of nothing, read on — it's less magic than you'd
think.

A speaker works by pushing a paper cone in and out. To play a sound, the
computer hands the speaker a long list of numbers: how far out the cone should
be, 44,100 times a second. That's all a sound file is. Everything below is
arithmetic for filling in that list.
"""

import array
import math

import pygame

RATE = 44100          # positions per second handed to the speaker
TABLE_SIZE = 2048     # how finely we draw one cycle of a wave
TARGET_RMS = 4200.0   # keeps every voice at roughly the same loudness
PEAK_CEILING = 26000  # leaves headroom so overlapping notes don't crackle

LETTER_STEPS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
NAMES_SHARP = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


# ---------- note names ----------

def note_number(name):
    """Turn a name like 'C4' or 'F#3' into a number. '-' means silence."""
    if name == "-":
        return None

    letter = name[0].upper()
    if letter not in LETTER_STEPS:
        raise ValueError(
            f"I don't understand the note {name!r}."
            "\nNotes look like C4, F#3 or Bb5. Use \"-\" for a rest."
        )

    step = LETTER_STEPS[letter]
    tail = name[1:]
    while tail and tail[0] in "#b":
        step += 1 if tail[0] == "#" else -1
        tail = tail[1:]

    if not tail.lstrip("-").isdigit():
        raise ValueError(
            f"The note {name!r} is missing its octave number."
            "\nTry C4 instead of C — 4 means the octave around middle C."
        )

    return (int(tail) + 1) * 12 + step


def note_name(number):
    """The other direction: 60 turns back into 'C4'."""
    return NAMES_SHARP[number % 12] + str(number // 12 - 1)


def frequency(number):
    """How many times per second the air shakes for this note."""
    return 440.0 * 2.0 ** ((number - 69) / 12.0)


# ---------- the shapes a sound can have ----------

def _build_table(kind):
    """Draw one single cycle of a wave. We reuse it for every note."""
    table = array.array("d", bytes(8 * TABLE_SIZE))
    for i in range(TABLE_SIZE):
        p = i / TABLE_SIZE
        if kind == "sine":
            value = math.sin(2 * math.pi * p)
        elif kind == "saw":
            value = 2.0 * p - 1.0
        elif kind == "square":
            value = 1.0 if p < 0.5 else -1.0
        else:                                   # "warm": a rounded-off saw
            value = (math.sin(2 * math.pi * p)
                     + 0.50 * math.sin(4 * math.pi * p)
                     + 0.33 * math.sin(6 * math.pi * p)
                     + 0.25 * math.sin(8 * math.pi * p)) / 2.08
        table[i] = value
    return table


TABLES = {k: _build_table(k) for k in ("sine", "saw", "square", "warm")}


# Each voice is a different set of dials on the same machine.
#
#   table         the shape of the wave: sine is soft, square is harsh
#   voices        how many copies play at once, slightly out of tune
#   detune        how far out of tune they are, in cents (100 cents = 1 semitone)
#   sub           how much of an extra note one octave down, for weight
#   octave_up     how much of an extra note one octave up, for bite
#   drive         how hard the sound is squashed. 1.0 is clean, 6.0 is nasty
#   cutoff_start  how bright the note starts. 1.0 is fully open
#   cutoff_end    how bright it ends. Lower means it darkens as it fades
#   attack        how long it takes to reach full volume, in seconds
#   decay         how long it takes to fade out, in seconds
#   glide         start this many cents flat and slide up to the real pitch
#   glide_ms      how long that slide takes
#   delay_ms      an echo: how long after the note the repeat arrives
#   delay_feedback how much of it comes back. 0.45 gives a few repeats
#
# The last two voices come from copying real instruments rather than inventing
# sounds. "moog" is modelled on a Memorymoog, a 1980s analogue synth that played
# several slightly-out-of-tune sawtooth waves at once — that's where the woozy,
# swelling quality comes from. "solo" copies an electric guitar put through so
# much processing that people mistake it for a synth; the giveaway is that it
# slides up into each note instead of stepping onto it, which is what "glide"
# does. Neither is tied to any particular song — they're just two sounds.
VOICES = {
    "bell":    dict(table="warm",   voices=1, detune=0,    sub=0.00, drive=1.0,
                    cutoff_start=1.00, cutoff_end=1.00, decay=0.90),
    "pluck":   dict(table="warm",   voices=1, detune=0,    sub=0.00, drive=1.6,
                    cutoff_start=0.35, cutoff_end=0.05, decay=0.45),
    "lead":    dict(table="saw",    voices=3, detune=14.0, sub=0.00, drive=3.2,
                    cutoff_start=0.30, cutoff_end=0.04, decay=1.10),
    "heavy":   dict(table="saw",    voices=3, detune=18.0, sub=0.55, drive=4.0,
                    cutoff_start=0.22, cutoff_end=0.03, decay=1.30),
    "searing": dict(table="square", voices=2, detune=10.0, sub=0.40, drive=6.0,
                    cutoff_start=0.16, cutoff_end=0.05, decay=1.60),
    "moog":    dict(table="saw",    voices=3, detune=9.0,  sub=0.35, drive=2.4,
                    cutoff_start=0.13, cutoff_end=0.06, decay=2.20,
                    attack=0.18, delay_ms=320, delay_feedback=0.34),
    "solo":    dict(table="saw",    voices=2, detune=12.0, sub=0.30, octave_up=0.30,
                    drive=5.5, cutoff_start=0.20, cutoff_end=0.05, decay=1.90,
                    glide=70.0, glide_ms=70.0, delay_ms=300,
                    delay_feedback=0.45),
}


def _render(freq, seconds, table, voices, detune, sub, drive,
            cutoff_start, cutoff_end, decay, attack=0.004, octave_up=0.0,
            glide=0.0, glide_ms=0.0,
            delay_ms=0.0, delay_feedback=0.0):
    total = int(RATE * seconds)
    wave = TABLES[table]
    sine = TABLES["sine"]
    mono = [0.0] * total

    # How far along the wave to step each sample, for each detuned copy.
    steps = []
    for v in range(voices):
        offset = 0.0 if voices == 1 else (v - (voices - 1) / 2.0) * detune
        steps.append(freq * (2.0 ** (offset / 1200.0)) * TABLE_SIZE / RATE)
    positions = [(v * TABLE_SIZE / voices) % TABLE_SIZE for v in range(voices)]

    sub_step = (freq / 2.0) * TABLE_SIZE / RATE
    up_step = (freq * 2.0) * TABLE_SIZE / RATE
    sub_pos = up_pos = 0.0

    # Sliding into the note: start flat and bend up to the real pitch.
    glide_samples = int(RATE * glide_ms / 1000.0)
    start_mult = 2.0 ** (-glide / 1200.0) if glide_samples else 1.0

    lowpass = 0.0
    share = 1.0 / voices
    tanh = math.tanh
    exp = math.exp
    loudness_fix = tanh(drive) if drive > 1.0 else 1.0
    cut_span = cutoff_end - cutoff_start

    for i in range(total):
        t = i / RATE

        bend = 1.0
        if i < glide_samples:
            bend = start_mult + (1.0 - start_mult) * (i / glide_samples)

        sample = 0.0
        for v in range(voices):
            p = positions[v]
            idx = int(p)
            a = wave[idx]
            b = wave[idx + 1 if idx + 1 < TABLE_SIZE else 0]
            sample += a + (b - a) * (p - idx)     # smooth between two points
            p += steps[v] * bend
            positions[v] = p - TABLE_SIZE if p >= TABLE_SIZE else p
        sample *= share

        if sub:
            sample += sub * sine[int(sub_pos)]
            sub_pos += sub_step * bend
            if sub_pos >= TABLE_SIZE:
                sub_pos -= TABLE_SIZE

        if octave_up:                             # an octave on top: "octave fuzz"
            sample += octave_up * wave[int(up_pos)]
            up_pos += up_step * bend
            if up_pos >= TABLE_SIZE:
                up_pos -= TABLE_SIZE

        envelope = exp(-t / decay)                # fade out like a plucked string
        if t < attack:
            envelope *= t / attack                # fade in, so it doesn't click
        sample *= envelope

        if drive > 1.0:                           # squash the peaks: distortion
            sample = tanh(sample * drive) / loudness_fix

        # Let less of the bright, buzzy part through as the note fades.
        lowpass += (cutoff_start + cut_span * (i / total)) * (sample - lowpass)
        mono[i] = lowpass

    # An echo. Adding a quieter copy of the past onto the present, in place,
    # means each echo also echoes — you get repeats that fade out on their own.
    step = int(RATE * delay_ms / 1000.0)
    if step and delay_feedback:
        for i in range(step, total):
            mono[i] += delay_feedback * mono[i - step]

    return mono


def _to_stereo(mono):
    """Even every voice out to the same loudness, then hand it to the speaker."""
    sampled = mono[::80]
    rms = math.sqrt(sum(v * v for v in sampled) / len(sampled)) if sampled else 0.0
    peak = max((abs(v) for v in mono), default=0.0)
    if rms < 1e-9 or peak < 1e-9:
        return array.array("h", bytes(4 * len(mono)))

    scale = (TARGET_RMS / 32000.0) / rms
    if peak * scale > PEAK_CEILING / 32000.0:
        scale = (PEAK_CEILING / 32000.0) / peak

    out = array.array("h", bytes(4 * len(mono)))
    for i, value in enumerate(mono):
        v = value * scale
        v = 1.0 if v > 1.0 else (-1.0 if v < -1.0 else v)
        s = int(v * 32000)
        out[2 * i] = s
        out[2 * i + 1] = s
    return out


def init_mixer():
    pygame.mixer.pre_init(RATE, -16, 2, 512)


def make_tone(freq, seconds=1.4, voice="bell"):
    """Build one playable note from scratch."""
    if voice not in VOICES:
        raise SystemExit(
            f"\nThere's no voice called {voice!r}."
            f"\nPick one of: {', '.join(sorted(VOICES))}\n"
        )
    mono = _render(freq, seconds, **VOICES[voice])
    return pygame.mixer.Sound(buffer=_to_stereo(mono).tobytes())
