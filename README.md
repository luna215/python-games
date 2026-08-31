# python-games

Python tutorials for Evolett. Each one opens a window with something moving in
it, and each lesson has a card telling you what to change and what to look for.

There are **two tutorials, and they're independent** — separate subjects, each
starting at its own lesson 1. Do them in either order, or only one. They share
nothing except the setup below.

Everything runs on your own computer. Nothing to sign up for, no website, and
after the one-time setup, no internet needed either.

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

## The two tutorials

**Run everything from this folder**, not from inside `pochita/` or
`melody-jumper/`.

### [Pochita](pochita/) — animation

One lesson. Pochita walks across the screen, and you find out that nothing is
moving: there are four drawings and some arithmetic.

| | Lesson | What it's really about | Time |
|---|---|---|---|
| **1** | [Pochita goes for a walk](pochita/LESSON1.md) | variables, and the fact that animation is just pictures swapped quickly | ~60 min |

```
./venv/bin/python pochita/lesson1.py
```

### [Melody Jumper](melody-jumper/) — music

One lesson. A ball bounces along platforms and plays a note on each landing. The
platforms are built out of the song itself, so what you see on screen is the
shape of the tune.

| | Lesson | What it's really about | Time |
|---|---|---|---|
| **1** | [The ball plays the song](melody-jumper/LESSON1.md) | a list of data driving everything you see *and* hear | ~75 min |

```
./venv/bin/python melody-jumper/jumper.py
```

---

## Controls

**ESC always quits.** Beyond that:

| | |
|---|---|
| **lesson1.py** | nothing to press. Pochita walks on his own. |
| **jumper.py** | `SPACE` pause · `R` start over |

---

## How a lesson works

Both tutorials follow the same shape. Read the lesson card first, then open the
`.py` file next to it.

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

You're in the wrong folder — probably inside a tutorial folder instead of this
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

Problems specific to one tutorial — missing sprites, no sound, a note name it
won't accept — are in that tutorial's own README:
[Pochita](pochita/README.md) · [Melody Jumper](melody-jumper/README.md).

---

## What's in here

```
pochita/            tutorial 1 — animation
  README.md
  LESSON1.md
  lesson1.py
  sprites/          18 files of Pochita artwork

melody-jumper/      tutorial 2 — music
  README.md
  LESSON1.md
  jumper.py
  tones.py          the sound engine

requirements.txt    what to install (just pygame-ce)
```

`pochita/` has artwork; `melody-jumper/` has no asset files at all, because every
note it plays is arithmetic worked out when the program starts.

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
rebuild it in seconds. It's already in `.gitignore` — leave it there.
