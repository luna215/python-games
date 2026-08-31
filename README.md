# python-games

Python projects for Evolett. Each one opens a window with something moving in
it, and each one has a card telling you what to change and what to look for.

Everything runs on your own computer. Nothing to sign up for, no website, and
after the one-time setup below, no internet needed either.

---

## Setup — you only do this once

Open **Terminal** (CMD+Space, type "Terminal", press Enter) and run these four
commands. Copy them one line at a time.

```
cd path/to/python-games
python3 -m venv venv
./venv/bin/pip install pygame-ce
./venv/bin/python pochita/lesson1.py
```

Replace `path/to/python-games` with wherever you cloned this repo. A shortcut:
type `cd ` (with the space), then drag the folder from Finder onto the Terminal
window, then press Enter.

A window should open with Pochita walking across it. **Press ESC to close it.**

That's the whole setup. From now on, running anything is just that last line
with a different file name.

### What those four commands did

| | |
|---|---|
| `cd …` | move into this folder |
| `python3 -m venv venv` | make a private Python just for this project, in a folder called `venv` |
| `./venv/bin/pip install pygame-ce` | download **pygame**, the library that opens windows and draws things (about 11 MB) |
| `./venv/bin/python pochita/lesson1.py` | run the program using that private Python |

The `./venv/bin/` prefix is the part people forget — see the first
troubleshooting entry below.

---

## The lessons

**Run everything from this folder**, not from inside `pochita/` or
`melody-jumper/`.

| | Lesson | What it's really about | Time |
|---|---|---|---|
| **1** | [Pochita goes for a walk](pochita/LESSON1.md) | variables, and the fact that animation is just pictures swapped quickly | ~60 min |
| **2** | [The ball plays the song](melody-jumper/LESSON2.md) | a list of data driving everything you see *and* hear | ~75 min |
| **3** | [Find the notes yourself](melody-jumper/LESSON3.md) | events — code that runs when something *happens* — and functions that hand back an answer | ~75 min |
| **4** | [The band](melody-jumper/LESSON4.md) | several things running at once against one clock, and lists of dictionaries | ~75 min |

```
./venv/bin/python pochita/lesson1.py
./venv/bin/python melody-jumper/jumper.py
./venv/bin/python melody-jumper/finder.py
./venv/bin/python melody-jumper/band.py
```

### How lessons 2, 3 and 4 fit together

They're one project seen three ways, and they share a single sound engine
(`tones.py`), so a change there changes all of them.

```
   finder.py  ──writes──▶  my_song.py  ──played by──▶  jumper.py
   (lesson 3)                                          (lesson 2)

   band.py    same tune, four instruments at once
   (lesson 4)
```

Lesson 2 plays one tune with one ball. Lesson 3 gives you a keyboard to hunt for
notes on, and saves whatever you work out into `my_song.py` — which lesson 2
then plays instead of its own tune, automatically. Lesson 4 puts four
instruments on screen together.

The order matters less than you'd think. If typing note names into a list in
lesson 2 starts to feel tedious, that tedium is exactly why lesson 3 exists — go
and do it, then come back.

---

## Controls

**ESC always quits.** Beyond that:

| | |
|---|---|
| **lesson1.py** | nothing to press. Pochita walks on his own. |
| **jumper.py** | `SPACE` pause · `R` start over |
| **band.py** | `SPACE` pause · `R` start over · `1` `2` `3` `4` mute an instrument |
| **finder.py** | `a w s e d f t g y h u j k o l p ;` the piano · `ENTER` keep the note you just played · `SPACE` hold for a silence · `BACKSPACE` delete the last one · `Z` `X` octave down/up · `Q` drone · `TAB` play back |

---

## How a lesson works

Read the lesson card first, then open the `.py` file next to it.

Every program is split in two. Everything you're meant to change sits at the top
under **YOUR CODE** — numbers, colours, the song, and one function with your name
on it. Underneath, **THE MACHINERY** is the plumbing that makes it run. You can
read the machinery, and some of it is genuinely interesting, but you never have
to touch it to do a lesson.

The rhythm is always the same:

> change one thing → **save the file** → run it again → look at what happened

Each card ends with a **Break it on purpose** section. Do those. Most of the
error messages in these programs were written specifically for the mistakes you
are about to make, which is not true of programming in general, and it's worth
seeing what a helpful error looks like before you meet the other kind.

---

## If something goes wrong

**`ModuleNotFoundError: No module named 'pygame'`**

You ran `python pochita/lesson1.py` instead of
`./venv/bin/python pochita/lesson1.py`. Your Mac's built-in Python doesn't have
pygame — only the private one in `venv` does, and the `./venv/bin/` prefix is
what picks it.

**`can't open file … [Errno 2] No such file or directory`**

You're in the wrong folder — probably inside a lesson folder instead of this
one. Run `pwd`; it should end in `python-games`. All the paths above start from
here.

**`command not found: python3`**

Your Mac doesn't have the developer tools yet. Run this, click through the
prompt, wait for it to finish, then try again:

```
xcode-select --install
```

**Nothing happens when I change a number**

The file isn't saved. ⌘-S in your editor, then run it again. This catches
everyone about four times and then never again.

**The window opened but I can't see it**

It's behind your other windows, or waiting in the Dock. Click the Python icon
there.

**`Can't find the 'sprites' folder`**

`lesson1.py` and the `sprites` folder have to sit next to each other inside
`pochita/`. If you moved one, put it back.

**There's no sound**

Check your volume and that nothing else has taken over the audio output. There
are no sound files to be missing — every note is built by the program when it
starts. You'll see a "building the sounds" bar while that happens: about a fifth
of a second for `jumper.py`, and a second or so for `band.py`, which builds 31
separate sounds because it needs one per pitch *per instrument*.

**The jumper is playing a different song than I expected**

If `my_song.py` exists, `jumper.py` plays that instead of its built-in tune, and
the corner of the window says `my_song.py` so you can tell. Delete that file to
go back, or set `USE_MY_SONG = False` at the top of `jumper.py`.

**The band takes ages before it sounds like anything**

That's deliberate. It starts with one instrument and adds another every four
bars, so all four are only playing after about 21 seconds. Look at `is_playing`
at the top of `band.py` — that's the function doing it.

---

## What's in here

```
pochita/            lesson 1
  lesson1.py
  LESSON1.md
  sprites/          18 files of Pochita artwork

melody-jumper/      lessons 2, 3 and 4 — everything to do with music
  jumper.py         lesson 2: one ball, one tune
  LESSON2.md
  finder.py         lesson 3: work out a song by ear
  LESSON3.md
  band.py           lesson 4: four instruments at once
  LESSON4.md
  tones.py          the sound engine, shared by all three
  my_song.py        not there yet — finder.py creates it

requirements.txt    what to install (just pygame-ce)
```

Inside `pochita/sprites/`:

- **`pochita_left_1..4.png`** and **`pochita_right_1..4.png`** — the eight
  drawings that make up the walk cycle. 45 pixels wide. Open one and you'll see
  the whole trick.
- **`pochita.svg`** — a still of him as vector art, so it stays sharp at any size.
- **`pochita-walk-*.svg`** — the same walk frames in vector form.
- **`pochita-reference.png`** — the original picture the sprites were traced from.

`melody-jumper/` has no asset files at all. Every note you hear is arithmetic,
worked out in `tones.py` when the program starts.

---

## About the music

The tune that comes with lessons 2 and 4 is **"In the Hall of the Mountain
King"**, written by Edvard Grieg in 1875. You've heard it — it's the creeping,
speeding-up one.

Those are Grieg's actual notes, taken off the score. Grieg died in 1907, so the
music belongs to everybody now, which is why they can be printed in a file here
rather than approximated.

That's also the honest reason it isn't a current song. Modern pop melodies are
almost never written down anywhere you can check, so anything claiming to be one
would be a guess. Working a song out by ear is the real way to get one — which
is the whole point of lesson 3, and why `jumper.py` will happily play whatever
Evolett finds instead.

---

## A note on Python versions

macOS ships with Python 3.9, and that's fine. `pip install pygame-ce` fetches
version 2.5.6, the newest that still supports 3.9, and everything here works with
it. Verified on a clean install.

If you have Python 3.10 or newer you'll get a slightly newer pygame instead.
Also fine.

---

## Don't commit the venv

The `venv` folder is about 40 MB of downloaded library, and the setup commands
rebuild it in seconds. It's already in `.gitignore` — leave it there. `my_song.py`
is *not* ignored, because that one is Evolett's work and worth keeping.
