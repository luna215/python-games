# Pochita goes for a walk

Change a few numbers, watch what each one does to him, then write the two
lines that stop him walking off the edge.

Change something → **Run it** → watch → **Back to the code**.
(Pressing ESC while it's running brings the code back too.)

<!-- step -->

## What's actually happening

Pochita isn't moving. There is no Pochita.

There are **four pictures** of him, and the computer is doing two things sixty
times a second:

1. adding a small number to where he is
2. drawing whichever picture is next

That's the entire trick behind every animated thing you have ever seen on a
screen. Four drawings and some arithmetic.

The drawings are real files, 45 pixels wide — smaller than this sentence is
tall. Everything else is the computer showing them to you fast.

<!-- step -->

## Faster. Slower.

Change `SPEED` to `1`, then **Run it**. Then try `10`. Then `40`.

At what point does he stop looking like he's walking and start looking like
he's being dragged?

<!-- step -->

## Backwards

Set `SPEED` to a negative number — `-3`, and run it.

He turns around. Look at the readout in the corner of the game: it says
`facing left` now.

The machinery picks a different set of four pictures depending on whether
`SPEED` is above or below zero. Nothing about *him* changed. A number went
below zero.

<!-- step -->

## Big and small

Try `SIZE = 1`. Then `SIZE = 12`.

Now notice what broke. At any size other than 5, his feet aren't on the ground
any more.

Fix it with `POCHITA_Y`. The ground is at **440**, and he is `27 * SIZE` pixels
tall — so what should `POCHITA_Y` be?

> Changing one number quietly broke something somewhere else. That is most of
> what debugging actually is.

<!-- step -->

## The legs

`FRAME_MS` is how long each picture is held, in milliseconds.

Try `20`. Then `400`. Then `2000`.

<!-- step -->

## The glide

Now the interesting one. Set `FRAME_MS = 2000` **and** `SPEED = 8`.

He *glides* — sliding across the floor with his legs barely moving, like he's
on ice.

Nothing is broken. His legs are changing far more slowly than he's travelling,
and your eye notices immediately. Real animators have a name for this and spend
real effort avoiding it.

Now find a `FRAME_MS` that makes `SPEED = 8` look like actual walking.

<!-- step -->

## Colour

Change `BACKGROUND`. It's `(red, green, blue)`, each from 0 to 255.

Make it night. Make it awful.

<!-- step -->

## Your turn

Right now, when Pochita reaches the edge he vanishes and reappears on the other
side. **Make him turn around instead.**

Where it says `# your turn goes here`, you need two `if` statements:

```python
    if x > 900 - 45 * SIZE:   # off the right edge
        speed = -speed        # same speed, other way

    if x < 0:                 # off the left edge
        speed = -speed
```

Type them in yourself rather than pasting — the shapes stick better that way.

He should now pace back and forth forever, turning at each wall. Turning around
means he faces the right way automatically.

**Why `-speed` and not `-3`?** Try `-3` in both places and watch him a while.

He turns at the right wall fine. At the left wall he doesn't — he walks straight
off and reappears on the right. Because there you told him "go left", and he was
already going left.

`-speed` means *the opposite of whatever you're doing now*. `-3` means one fixed
direction, which is only right half the time.

<!-- step -->

## Break it on purpose

Do these. Most of the error messages here were written for the exact mistakes
you're about to make, which is **not** true of programming in general.

Anything the lesson saw coming comes up **yellow**. Anything it didn't comes up
**red** — that's ordinary Python, talking to you the way it talks to everybody.

**These three stop the program and tell you why:**

1. Delete the `return x, speed` line at the bottom.
2. Put it back. Change `BACKGROUND` to `(246, 234, 999)`.
3. Rename `move` to `Move`, with a capital M.

Number 3 is worth doing properly. `move` and `Move` are two completely different
things to Python, and it will not guess what you meant.

**This one says nothing at all:**

4. Change `SIZE = 5` to `SIZE = 5.5`.

No error. But look closely — his pixels have gone uneven, some fatter than
others. He's `45 * 5.5 = 247.5` pixels wide, there's no such thing as half a
pixel, so the computer quietly threw the `.5` away.

Nothing warned you. It never does. **Change one number, look at the result** —
that habit catches more bugs than any error message will.
