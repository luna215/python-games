# Pochita

A one-lesson tutorial about animation.

Pochita walks across a window. Nothing is actually moving — there are four
drawings of him and some arithmetic, which turns out to be the whole trick
behind every animated thing you have ever seen.

**You don't need to have done the [Melody Jumper tutorial](../melody-jumper/)
first.** This one starts from the beginning, and the two don't depend on each
other.

---

## Setup

If you've already run the four commands in the [main README](../README.md),
you're done — skip to the lesson.

If not, from the `python-games` folder (the one *above* this one):

```
python3 -m venv venv
./venv/bin/pip install pygame-ce
```

That's it. One library, about 11 MB.

---

## The lesson

Run it from the `python-games` folder, not from inside this one.

| | Lesson | What it's really about | Time |
|---|---|---|---|
| **1** | [Pochita goes for a walk](LESSON1.md) | variables, and the fact that animation is just pictures swapped quickly | ~60 min |

```
./venv/bin/python pochita/lesson1.py
```

**ESC quits.** There's nothing else to press — Pochita walks on his own, and the
lesson is about changing the numbers that decide *how*.

---

## How the lesson works

Read the lesson card first, then open `lesson1.py` next to it.

The program is split in two. Everything you're meant to change sits at the top
under **YOUR CODE** — numbers, colours, and one function with your name on it.
Underneath, **THE MACHINERY** is the plumbing that makes it run. You can read the
machinery, and some of it is genuinely interesting, but you never have to touch
it to do the lesson.

The rhythm is always the same:

> change one thing → **save the file** → run it again → look at what happened

The card ends with a **Break it on purpose** section. Do those. Most of the
error messages in this program were written for the exact mistakes you're about
to make, which is not true of programming in general — it's worth seeing what a
helpful error looks like before you meet the other kind.

---

## What's in here

```
lesson1.py    the program — run this
LESSON1.md    what to do, and why
sprites/      18 files of artwork
```

Inside `sprites/`:

- **`pochita_left_1..4.png`** and **`pochita_right_1..4.png`** — the eight
  drawings that make up the walk cycle. 45 pixels wide. Open one and you'll see
  the whole trick.
- **`pochita.svg`** — a still of him as vector art, so it stays sharp at any size.
- **`pochita-walk-*.svg`** — the same walk frames in vector form, for anything
  that isn't this program.
- **`pochita-reference.png`** — the original picture the sprites were traced from.

`lesson1.py` and the `sprites` folder have to stay next to each other. If you
move one, the program will tell you it can't find the artwork.

---

## Where the artwork came from

The sprites were traced from a reference image by hand, pixel by pixel, and the
walk cycle was built by moving the legs between frames.

That process had exactly the bug challenge 5 in the lesson is about: at one point
his feet slid along the ground instead of stepping, because the legs were
changing more slowly than he was travelling. Animators have a name for it and
spend real effort avoiding it. It's worth seeing on purpose.
