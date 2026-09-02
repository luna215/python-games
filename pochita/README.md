# Pochita

A tutorial about making games, starting from nothing.

Lesson 1 is an animation: Pochita walks, and you watch. Lesson 2 hands you the
controls, and that one change — you deciding instead of a number deciding — is
the whole difference between a film and a game.

**You don't need to have done the [Melody Jumper tutorial](../melody-jumper/)
first.** This one starts from the beginning, and the two don't depend on each
other.

---

## Setup

If you've already run the four commands in the [main README](../README.md),
you're done — skip to the lessons.

If not, from the `python-games` folder (the one *above* this one):

```
python3 -m venv venv
./venv/bin/pip install pygame-ce
```

That's it. One library, about 11 MB.

---

## The lessons

Run these from the `python-games` folder, not from inside this one.

| | Lesson | What it's really about | Time |
|---|---|---|---|
| **1** | [Pochita goes for a walk](LESSON1.md) | variables, and the fact that animation is just pictures swapped quickly | ~60 min |
| **2** | [Pochita goes looking for bread](LESSON2.md) | input — a program that reacts instead of replaying — and a second number that doesn't behave how you'd expect | ~75 min |

```
./venv/bin/python pochita/lesson1.py
./venv/bin/python pochita/lesson2.py
```

**ESC quits both.** Lesson 1 has nothing else to press — Pochita walks on his
own, and the lesson is about changing the numbers that decide how. Lesson 2 is
driven with the **arrow keys**.

Where it's going: two players, then a game they can win. Each lesson adds one
idea and leaves you with something that runs.

---

## How these lessons work

Read the lesson card first, then open the `.py` file next to it.

Every program is split in two. Everything you're meant to change sits at the top
under **YOUR CODE** — numbers, colours, and one or two functions with your name
on them. Underneath, **THE MACHINERY** is the plumbing that makes it run. You can
read the machinery, and some of it is genuinely interesting, but you never have
to touch it to do a lesson.

The rhythm is always the same:

> change one thing → **save the file** → run it again → look at what happened

Each card ends with a **Break it on purpose** section. Do those. Most of the
error messages in these programs were written for the exact mistakes you're
about to make, which is not true of programming in general — it's worth seeing
what a helpful error looks like before you meet the other kind.

---

## What's in here

```
lesson1.py    Pochita walks
LESSON1.md
lesson2.py    you drive him, and he wants bread
LESSON2.md
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

The lesson files and the `sprites` folder have to stay next to each other. If you
move one, the program will tell you it can't find the artwork.

There are only drawings of him facing **left and right** — nobody drew a Pochita
seen from behind. From lesson 2 onwards he's viewed from above and can walk up
and down, and he'll keep facing sideways while he does it. Most top-down games do
exactly that; it's worth knowing so it doesn't look like a bug.

---

## Where the artwork came from

The sprites were traced from a reference image by hand, pixel by pixel, and the
walk cycle was built by moving the legs between frames.

That process had exactly the bug challenge 5 in lesson 1 is about: at one point
his feet slid along the ground instead of stepping, because the legs were
changing more slowly than he was travelling. Animators have a name for it and
spend real effort avoiding it. It's worth seeing on purpose.
