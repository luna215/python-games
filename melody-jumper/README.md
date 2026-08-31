# Melody Jumper

A tutorial about making music with code.

A ball bounces along a row of platforms and plays a note every time it lands.
The platforms aren't placed by hand — they're built out of the song itself, so
the shape you see on screen *is* the shape of the tune.

**You don't need to have done the [Pochita tutorial](../pochita/) first.** This
one starts from the beginning.

---

## Setup

If you've already run the four commands in the [main README](../README.md),
you're done — skip to the lesson.

If not, from the `python-games` folder (the one *above* this one):

```
python3 -m venv venv
./venv/bin/pip install pygame-ce
```

That's it. One library, about 11 MB, and no internet needed afterwards.

---

## The lesson

Run it from the `python-games` folder, not from inside this one.

| | Lesson | What it's really about | Time |
|---|---|---|---|
| **1** | [The ball plays the song](LESSON1.md) | a list of data driving everything you see *and* hear | ~75 min |

```
./venv/bin/python melody-jumper/jumper.py
```

**ESC** quits · **SPACE** pauses · **R** starts the song over.

---

## How the lesson works

Read the lesson card first, then open `jumper.py` next to it.

The program is split in two. Everything you're meant to change sits at the top
under **YOUR CODE** — the song, the tempo, how the notes sound, the colours, and
one function with your name on it. Underneath, **THE MACHINERY** is the plumbing
that makes it run. You can read the machinery, and some of it is genuinely
interesting, but you never have to touch it to do the lesson.

The rhythm is always the same:

> change one thing → **save the file** → run it again → look at what happened

The card ends with a **Break it on purpose** section. Do those. Most of the error
messages in this program were written for the exact mistakes you're about to
make, which is not true of programming in general — it's worth seeing what a
helpful error looks like before you meet the other kind.

---

## What's in here

```
jumper.py     the program — run this
LESSON1.md    what to do, and why
tones.py      the sound engine
```

There are **no asset files** in this folder. No sound files, nothing to
download. Every note you hear is arithmetic, worked out in `tones.py` when the
program starts — which is why you'll see a "building the sounds" bar for a
moment on startup.

`tones.py` is worth a look once the lesson makes sense. The `VOICES` table near
the top is seven different sounds built from the same machine with the dials set
differently, and the comment above it says what every dial does.

---

## About the music

The tune that comes with it is **"In the Hall of the Mountain King"**, written by
Edvard Grieg in 1875. You've heard it — it's the creeping, speeding-up one.

Those are Grieg's actual notes, taken off the score. He died in 1907, so the
music belongs to everybody now, which is why they can sit in a file here rather
than being approximated.

That's also the honest reason it isn't a current song. Modern pop melodies are
almost never written down anywhere you can check, so anything claiming to be one
would be a guess. If you want a song from this decade in there, the way to get it
is to work it out by ear, one note at a time, and type it into `MELODY` yourself.

---

## If something goes wrong

**There's no sound.** Check your volume and that nothing else has taken over the
audio output. There are no sound files to be missing — startup takes about a
fifth of a second to build them, and you'll see a bar while it happens.

**I changed a note and nothing happened.** The file isn't saved. ⌘-S, then run it
again.

**It says it doesn't understand one of my notes.** Note names are a letter, an
optional `#` or `b`, and an octave number: `C4`, `F#3`, `Bb5`. Use `"-"` for a
rest. The error message names the note it choked on.

Everything else — `ModuleNotFoundError`, wrong folder, no `python3` — is in the
[main README](../README.md).
