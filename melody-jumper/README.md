# Melody Jumper

A three-lesson tutorial about making music with code.

A ball bounces along a row of platforms and plays a note every time it lands. By
the end you'll have taught it a song you worked out by ear, and put four
instruments on screen playing together.

**You don't need to have done the [Pochita tutorial](../pochita/) first.** This
one starts from the beginning.

---

## Setup

If you've already run the four commands in the [main README](../README.md),
you're done — skip to the lessons.

If not, from the `python-games` folder (the one *above* this one):

```
python3 -m venv venv
./venv/bin/pip install pygame-ce
```

That's it. One library, about 11 MB, and no internet needed afterwards.

---

## The lessons

Run these from the `python-games` folder, not from inside this one.

| | Lesson | What it's really about | Time |
|---|---|---|---|
| **1** | [The ball plays the song](LESSON1.md) | a list of data driving everything you see *and* hear | ~75 min |
| **2** | [Find the notes yourself](LESSON2.md) | events — code that runs when something *happens* — and functions that hand back an answer | ~75 min |
| **3** | [The band](LESSON3.md) | several things running at once against one clock, and lists of dictionaries | ~75 min |

```
./venv/bin/python melody-jumper/jumper.py
./venv/bin/python melody-jumper/finder.py
./venv/bin/python melody-jumper/band.py
```

### How they connect

```
   finder.py  ──writes──▶  my_song.py  ──played by──▶  jumper.py
   (lesson 2)                                          (lesson 1)

   band.py    the same tune, four instruments at once
   (lesson 3)
```

Lesson 1 plays one tune with one ball. Lesson 2 gives you a keyboard to hunt for
notes on, and saves whatever you work out into `my_song.py` — which lesson 1 then
plays instead of its own tune, automatically, the next time you run it. Lesson 3
puts four instruments on screen together.

All three share one sound engine, `tones.py`, so a change there changes all of
them.

---

## How these lessons work

Read the lesson card first, then open the `.py` file next to it.

Every program is split in two. Everything you're meant to change sits at the top
under **YOUR CODE** — numbers, colours, and one function with your name on it.
Underneath, **THE MACHINERY** is the plumbing that makes it run. You can read the
machinery, and some of it is genuinely interesting, but you never have to touch
it to do a lesson.

The rhythm is always the same:

> change one thing → **save the file** → run it again → look at what happened

Each card ends with a **Break it on purpose** section. Do those. Most of the
error messages in these programs were written for the exact mistakes you're
about to make, which is not true of programming in general — it's worth seeing
what a helpful error looks like before you meet the other kind.

---

## Controls

**ESC always quits.**

| | |
|---|---|
| **jumper.py** | `SPACE` pause · `R` start over |
| **band.py** | `SPACE` pause · `R` start over · `1` `2` `3` `4` mute an instrument |
| **finder.py** | `a w s e d f t g y h u j k o l p ;` the piano · `ENTER` keep the note you just played · `SPACE` hold for a silence · `BACKSPACE` delete the last one · `Z` `X` octave down/up · `Q` drone · `TAB` play back what you've kept |

The finder's piano layout is the one GarageBand and Ableton use. `R` and `I` are
deliberately not on it, because there's no black key between E and F, or between
B and C.

---

## What's in here

```
jumper.py     lesson 1: one ball, one tune
LESSON1.md
finder.py     lesson 2: work out a song by ear
LESSON2.md
band.py       lesson 3: four instruments at once
LESSON3.md
tones.py      the sound engine, shared by all three
my_song.py    not there yet — finder.py creates it
```

There are **no asset files** in this folder. No sound files, nothing to
download. Every note you hear is arithmetic, worked out in `tones.py` when the
program starts — which is why you'll see a "building the sounds" bar for a
moment on startup.

---

## About the music

The tune that comes with lessons 1 and 3 is **"In the Hall of the Mountain
King"**, written by Edvard Grieg in 1875. You've heard it — it's the creeping,
speeding-up one.

Those are Grieg's actual notes, taken off the score. He died in 1907, so the
music belongs to everybody now, which is why they can sit in a file here rather
than being approximated.

That's also the honest reason it isn't a current song. Modern pop melodies are
almost never written down anywhere you can check, so anything claiming to be one
would be a guess. Working a song out by ear is the real way to get one — which
is the whole point of lesson 2, and why `jumper.py` will happily play whatever
you find instead.

---

## If something goes wrong

**There's no sound.** Check your volume and that nothing else has taken over the
audio output. There are no sound files to be missing. Startup takes about a
fifth of a second for `jumper.py` and a second for `band.py`, which builds 31
separate sounds because it needs one per pitch *per instrument*.

**The jumper is playing a different song than I expected.** If `my_song.py`
exists, `jumper.py` plays that instead of its built-in tune, and the corner of
the window says `my_song.py` so you can tell. Delete that file to go back, or set
`USE_MY_SONG = False` at the top of `jumper.py`.

**The band takes ages before it sounds like anything.** That's deliberate. It
starts with one instrument and adds another every four bars, so all four are only
playing after about 21 seconds. Look at `is_playing` at the top of `band.py` —
that's the function doing it.

Everything else — `ModuleNotFoundError`, wrong folder, no `python3` — is in the
[main README](../README.md).
