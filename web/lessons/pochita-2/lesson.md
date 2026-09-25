# Bread and jam

Lesson 1 was a film — Pochita walked because a number said so, and you watched.
This is a game, and the difference is you.

Fetch Denji one bread **and** one jam and he'll come out and eat. One of the two
you can reach. The other you can't, and working out why is the whole lesson.

<!-- step -->

## Play it first

Press **Run it** and use the **arrow keys** (WASD works too).

Play for a minute. You'll get the bread. You won't get the jam, however hard you
mash the keys — the counter sits at `jam 0 / 1` and Denji never shows up.

**Work out why before you read on.**

<!-- step -->

## What's going on

Lesson 1 ran on its own. Now the machinery asks *what are you holding down right
now?* sixty times a second and hands your code the answer.

It tells you through `keys`:

```python
keys["left"]    # True if left is down right now, otherwise False
```

Four labels — `"left"`, `"right"`, `"up"`, `"down"` — each either `True` or
`False`. The top-left of the game shows what's in it as you play.

And there are two numbers now instead of one: `x` is how far across, `y` is how
far down.

He faces sideways even when walking up or down. There are only left and right
drawings of him — most top-down games do the same, so it isn't a bug.

<!-- step -->

## Your turn — get the jam

The **bread** lands somewhere on the row he's standing on. The **jam** lands in
his column, directly above or below him.

Look at `move`. There's a left and a right. There is no up and no down — and
up-or-down is the only direction the jam ever appears in.

**Add the other two**, the same shape as the two already there, using
`keys["up"]` and `keys["down"]`, and changing `y` instead of `x`.

Put them **above** the `return x, y` line. Anything below a `return` never runs,
and the game would behave exactly as if you'd typed nothing.

**Decide which way up is before you run it.** Say your guess out loud, then hold
the up arrow.

<!-- step -->

## Which way is up

On a screen, `y` counts *downwards*. `y = 0` is the top row of pixels, `y = 600`
is the bottom — so up means making `y` **smaller**.

Everyone gets this wrong once and then never again.

<!-- step -->

## Speed

Try `SPEED` at `1`, then `20`, then push it past sensible. Bread collected in
fifteen seconds of running wall to wall:

| SPEED | 4 | 20 | 120 | **150** | **200** |
| --- | --- | --- | --- | --- | --- |
| bread | 4.7 | 24.2 | 118.1 | **2.8** | **1.0** |

Faster is better and better — then at 150 it falls off a cliff. Leave it running
and watch: he grabs a couple, then never gets another one. He's stuck.

`REACH` is 50, so he has to get within 50 pixels. At `SPEED = 150` he jumps 150
pixels a frame, so the spots he can *ever* stand on are a coarse grid, and the
bread is sitting in a gap between them. The closest he ever gets is 56 pixels.
Six pixels short, forever.

That's a real bug with a real name — **tunnelling** — and it's why a fast enough
bullet sometimes goes straight through a wall.

**Put `SPEED` back to 4.**

<!-- step -->

## The diagonal is faster

Hold `right`. Then hold `right` and `up` together.

About 240 pixels in a second against about 340. A ratio of 1.4142, which is √2 —
because he moved `SPEED` across *and* `SPEED` down in the same frame, and the
corner-to-corner distance is longer than either side.

Most games have had this bug at some point.

<!-- step -->

## Reach

`REACH` is how close his middle has to get to a thing's middle.

Try `10`. Then `200`. Then put it back to `50` — the next two steps need it
there.

<!-- step -->

## Break the touching test

In `is_touching`, delete the second half so it only checks `x`:

```python
    return abs(ax - bx) < REACH
```

Now **stand still and don't touch the keyboard** for ten seconds:

| checks | bread | jam |
| --- | --- | --- |
| both (as shipped) | 0 | 0 |
| only `x` | 0 | **601** |
| only `y` | **601** | 0 |

Six hundred jars without moving. The jam is always in his column, so once you
stop checking the vertical distance he's touching it the moment it appears,
sixty times a second.

Denji still won't come out, though — he needs one of *each*, and the other
counter is stuck on zero.

<!-- step -->

## The real one

Put it back, then try this instead:

```python
    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5 < REACH
```

That's the distance formula from maths class — the hypotenuse — and it's
genuinely how games decide whether you got hit. With `REACH = 50`:

| gap | what you started with | the distance version | really apart |
| --- | --- | --- | --- |
| 49 across, 0 down | touching | touching | 49 px |
| 35 across, 35 down | touching | touching | 49 px |
| **49 across, 49 down** | **touching** | **not touching** | **69 px** |

The first version draws an invisible *square* round him, and a square's corners
sit further out than its sides — so he can eat something 69 pixels away as long
as it's diagonal. The distance version draws a *circle*, which is the same
distance all the way round.

<!-- step -->

## Make it a real game

**`NEEDED = 5`.** How many of each he has to fetch before Denji appears. One
number turns a thirty-second game into an actual one.

This is your first design decision rather than a bug fix. There's no right
answer.

**`WIN_MESSAGE`.** Change what Denji says when he comes out. Long ones wrap by
themselves.

**`SIZE` and `BACKGROUND`** work the same as they did in lesson 1.

<!-- step -->

## Break it on purpose

Anything the lesson saw coming comes up **yellow**. Anything it didn't comes up
**red** — that's ordinary Python.

**These five stop the program and tell you what you did:**

1. Delete `return x, y` from the bottom of `move`.
2. Put it back, then change it to `return x`.
3. Ask for `keys["Up"]` with a capital U.
4. Delete the `return` from the line in `is_touching`.
5. Set `NEEDED = 0`.

Number 3 is worth reading properly. `"up"` and `"Up"` are two different things
to Python, and it will not guess what you meant.

**This one says nothing at all:**

6. Set `REACH = 200` and play. **Watch him, not the score.**

No error, and the score barely changes — what slows him down is running about,
not reaching. But look at what he's doing: he snatches things from two
body-lengths away without going near them.

The program did exactly what you asked. It's your idea of the game that's
broken, and no error can catch that.
