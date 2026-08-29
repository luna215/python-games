# Lesson 1 — Pochita goes for a walk

**The fundamental:** variables, and the idea that animation is just pictures
swapped quickly.
**Time:** ~60 min. **File:** [lesson1.py](lesson1.py)

---

## Run it

```
./venv/bin/python pochita-game/lesson1.py
```

A window opens and Pochita walks across it. Press **ESC** or close the window to
stop him.

This is the first thing you're running on your own computer instead of in a
browser tab. Same deal as the notebooks: change something, **save the file**,
run it again, look at what happened.

---

## What's actually happening

Pochita isn't moving. There is no Pochita.

There are **four pictures** of him, and the computer is doing two things sixty
times a second:

1. adding a small number to where he is
2. drawing whichever picture is next

That's the entire trick behind every animated thing you have ever seen on a
screen. Four drawings and some arithmetic.

Open the `sprites` folder and look at `pochita_left_1.png` through
`pochita_left_4.png`. They're 45 pixels wide. Everything else is the computer
showing them to you fast.

---

## Challenges

**1. Faster. Slower.** Change `SPEED` to 1. Then 10. Then 40. At what point does
he stop looking like he's walking and start looking like he's being dragged?

**2. Backwards.** Set `SPEED` to a negative number — `-3`. He turns around.

Look at the HUD in the corner: it says `facing left` now. The machinery picks a
different set of four pictures depending on whether `SPEED` is positive or
negative. Nothing about *him* changed; a number went below zero.

**3. Big and small.** `SIZE = 1`. Then `SIZE = 12`.

Now notice what broke: at any size other than 5, his feet aren't on the ground
any more. Fix it with `POCHITA_Y`. (The ground is at 440, and he's `27 * SIZE`
pixels tall. So what should `POCHITA_Y` be?)

**4. The legs.** `FRAME_MS` is how long each picture is held. Try `20`. Then
`400`. Then `2000`.

**5. Now the interesting one.** Set `FRAME_MS = 2000` and `SPEED = 8`.

He *glides* — sliding across the floor with his legs barely moving, like he's on
ice. Nothing is broken. His legs are just changing far more slowly than he's
travelling, and your eye notices immediately.

Real animators have a name for this and spend real effort avoiding it. Now find
a `FRAME_MS` that makes `SPEED = 8` look like actual walking.

**6. Colour.** Change `BACKGROUND`. Make it night. Make it awful.

---

## Your turn

Right now, when Pochita reaches the edge he vanishes and reappears on the other
side. **Make him turn around instead.**

Find the `move` function. You need two `if` statements:

```python
    if x > 900 - 45 * SIZE:      # gone off the right edge
        speed = -speed           # same speed, other direction

    if x < 0:                    # gone off the left edge
        speed = -speed
```

Type them in yourself rather than pasting — the shapes stick better that way.

Then run it. He should pace back and forth forever, turning around at each wall,
and turning around means he faces the right way automatically.

**Why `-speed` and not `-3`?** Try `-3` in both places and watch him for a while.

He turns around fine at the right wall. At the left wall he doesn't — he walks
straight off the edge and reappears on the right. Because at the left wall you
told him "go left", and he was already going left.

`-speed` means *the opposite of whatever you're doing now*. `-3` means one fixed
direction, which is only ever right half the time.

---

## Break it on purpose

**These three stop the program and tell you why:**

1. Delete the `return x, speed` line at the bottom of `move`.
2. Put it back. Change `BACKGROUND` to `(246, 234, 999)`.
3. Rename the `sprites` folder to `sprite`, run it, then rename it back.

Number 3 is worth doing properly. Programs depend on files being exactly where
they expect. That message is the machinery telling you politely; most of the
time you'd get a wall of red text instead.

**This one says nothing at all:**

4. Change `SIZE = 5` to `SIZE = 5.5`.

No error. But look closely at him — the pixels have gone uneven, some fatter
than others. He's `45 * 5.5 = 247.5` pixels wide, and there's no such thing as
half a pixel, so the computer quietly threw the .5 away and squashed him into
247.

Nothing warned you. It never does. **Change one number, look at the result** —
that habit catches more bugs than any error message will.

---

## Teacher notes

**The one concept:** a variable is a number with a name, and changing it changes
what you see. Same as notebook lesson 1 — but now it moves, which lands
differently.

**Setup, first time only.** They need Python and pygame on the machine. From the
`dev-games` folder:

```
python3 -m venv venv
./venv/bin/pip install pygame-ce
```

**Expect these:**

- *Nothing happened.* Unsaved file. It happens to everyone about four times.
- *Challenge 3 (feet off the ground).* The point isn't the arithmetic, it's
  noticing that changing one number quietly broke something somewhere else.
  That's most of debugging.
- *Challenge 5 (the glide).* Worth dwelling on. Ask them what looks wrong before
  explaining it — "his legs aren't keeping up" is exactly right, and it's a real
  thing animators fight. This same bug happened while making these sprites.
- *`-speed` vs `-3`.* With `-3` hardcoded he bounces off the right wall
  correctly, then sails straight off the left edge and wraps around — because
  "go left" is already what he was doing. Verified: x reaches -188. A good
  half-working bug; the fix has to depend on current state, not a fixed value.
- *`SIZE = 5.5` doesn't error.* It truncates to 247 pixels wide and the pixel
  grid goes uneven. Another silent one — same family as the notebook lessons.

**If they ask where the pictures came from:** they were traced from a reference
image, pixel by pixel, and the walk cycle was built by moving the legs. The
`.svg` files in `sprites` are the same drawings in a format that scales without
going blurry.

**End of session:** screenshot into `progress/`.

---

## Next lesson

Pochita walks where the number tells him to. Next time **you** tell him — arrow
keys, and he goes where you point.
