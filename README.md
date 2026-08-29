# python-games — Pochita lessons

This is so Evolett can learn programming with the help from pochita.

Everything runs on your own computer. Nothing to sign up for, no website.

---

## Getting started on a Mac

Open **Terminal** (CMD+Space, type "Terminal", Enter) and run these four commands.
Copy them one line at a time.

```
cd path/to/python-games
python3 -m venv venv
./venv/bin/pip install pygame-ce
./venv/bin/python lesson1.py
```

Replace `path/to/python-games` with wherever you cloned this repo. A shortcut:
type `cd `, then drag the folder from Finder onto the Terminal window, then
press Enter.

A window should open with Pochita walking across it. **Press ESC to close it.**

That's the whole setup. You only do it once — after that, running a lesson is
just the last line.

### What those commands did

| | |
|---|---|
| `cd …` | move into this folder |
| `python3 -m venv venv` | make a private Python just for this project, in a folder called `venv` |
| `./venv/bin/pip install pygame-ce` | download **pygame**, the library that opens the window and draws things |
| `./venv/bin/python lesson1.py` | run the lesson using that private Python |

The `./venv/bin/` part matters — see the first troubleshooting entry below.

---

## The lessons

| | |
|---|---|
| **[Lesson 1 — Pochita goes for a walk](LESSON1.md)** | variables, and how animation actually works |

Read the lesson card, then open the `.py` file. Everything you're meant to
change is at the top under **YOUR CODE**. The part underneath marked
**THE MACHINERY** is the plumbing — you can read it, but you don't need to.

The rhythm is always: change something → **save the file** → run it again → look
at what happened.

---

## If something goes wrong

**`ModuleNotFoundError: No module named 'pygame'`**

You ran `python lesson1.py` instead of `./venv/bin/python lesson1.py`. Your
Mac's built-in Python doesn't have pygame — only the private one in `venv` does.
The `./venv/bin/` prefix is what picks it.

**`command not found: python3`**

Your Mac doesn't have the developer tools yet. Run this, click through the
prompt, wait for it to finish, then try again:

```
xcode-select --install
```

**Nothing happens when I change a number**

The file isn't saved. ⌘-S in your editor, then run it again. This catches
everyone roughly four times and then never again.

**The window opened but I can't see it**

It's probably behind your other windows, or in the Dock. Click the Python icon
there.

**`Can't find the 'sprites' folder`**

The lesson file and the `sprites` folder have to sit next to each other. If you
moved one, put it back.

---

## What's in here

```
lesson1.py       the first lesson — run this
LESSON1.md       what to do, and why
requirements.txt what to install
sprites/         all the Pochita artwork
```

Inside `sprites/`:

- **`pochita_left_1..4.png`** and **`pochita_right_1..4.png`** — the eight
  drawings that make up the walk cycle. 45 pixels wide. Open one and you'll see
  the whole trick.
- **`pochita.svg`** — a still of him, as vector art, so it stays sharp at any
  size.
- **`pochita-walk-*.svg`** — the same walk frames in vector form, for anything
  that isn't this game.
- **`pochita-reference.png`** — the original picture the sprites were traced
  from.

---

## A note on Python versions

macOS ships with Python 3.9. That's fine — `pip install pygame-ce` will fetch
version 2.5.6, which is the newest one that supports 3.9, and every lesson here
works with it. Verified on a clean install.

If you have Python 3.10 or newer you'll get a slightly newer pygame instead.
That's also fine.

---

## Don't commit the venv

The `venv` folder is a few hundred megabytes and is rebuilt by the commands
above in about thirty seconds. If this is in a git repo, keep it ignored — the
`.gitignore` here already does that.
