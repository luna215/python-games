# Lesson 2 — Pochita goes looking for bread

**The fundamental:** input. A program that *reacts* instead of one that replays.
And a second number, `y`, which turns out not to work the way you'd expect.
**Time:** ~75 min. **File:** [lesson2.py](lesson2.py)

---

## Run it

```
./venv/bin/python pochita/lesson2.py
```

**Arrow keys** move him. **ESC** quits.

Try it before you read any further. He goes left and right and refuses to go up
or down, and there's a piece of bread he can't reach. Fixing that is the lesson.

---

## What's actually happening

### Lesson 1 was a film. This is a game.

In lesson 1, Pochita walked because `SPEED` said so. You could change the number
and watch a different film, but while it was running you were a spectator.

Now the machinery asks a question sixty times a second — *what is she holding
down right now?* — and hands your code the answer. That's the entire difference
between an animation and a game, and it's why every game ever made has a loop
like this one at its heart.

### The camera moved

The floor is gone. Lesson 1 watched him from the side, like a side-on photo, so
there was a ground line and he walked along it. This one looks straight down at
him from above, which is why he can now go in four directions instead of two.

He'll still face sideways when he walks up or down — there are only drawings of
him facing left and right, and nobody drew a Pochita seen from the back. Most
top-down games do exactly this and you stop noticing within a minute.

### `keys`

Your `move` function gets handed something called `keys`. You ask it questions:

```python
keys["left"]      # True if the left arrow is down RIGHT NOW, otherwise False
```

Four labels — `"left"`, `"right"`, `"up"`, `"down"` — and each one is either
`True` or `False`. Not "was it pressed at some point", but "is it down at this
exact instant". That's why holding a key moves him smoothly: the question gets
asked again sixty times a second and the answer keeps coming back `True`.

Look at the bottom-left corner of the window while you play. It shows you
exactly what's in `keys` at that moment.

### Two numbers now

Lesson 1 had `x`: how far across. This has `x` **and** `y`: how far across, and
how far down. Together they say exactly where the middle of him is, and the
corner of the window shows you both while you move.

---

## Your turn — give him up and down

This is the main event, and it's four lines.

Open `lesson2.py` and find `move`. Two of the four directions are already
written:

```python
    if keys["left"]:
        x = x - SPEED

    if keys["right"]:
        x = x + SPEED
```

Add two more, the same shape, using `keys["up"]` and `keys["down"]` — and
changing `y` instead of `x`.

**Before you run it, decide which way up is.** Write down your guess. Then run
it and hold the up arrow.

<br>

**If he went the wrong way, you are in good company.** On a screen, `y` counts
*downwards* from the top. `y = 0` is the very top row of pixels and `y = 600` is
the bottom. So going up means making `y` **smaller** — subtracting, not adding.

The reason is history: the first screens drew the picture one line at a time,
starting at the top and sweeping down, and the numbering followed the sweep.
Every screen since has kept it, so the graph paper from maths class is upside
down here. This trips up absolutely everyone once, and then never again.

Now go and get the bread.

---

## Challenges

**1. Speed.** `SPEED = 1`. Then `20`. Then `60`. He covers 244 pixels a second
at the shipped 4, so at 60 he's across the room in a blink — but he still eats
everything he runs into.

Now push it further, and walk him straight at the bread from a distance:

| SPEED | does he eat it? |
| --- | --- |
| 60 | yes |
| 100 | yes |
| 101 | yes |
| **120** | **no — straight over the top of it** |
| 150 | yes |
| **200** | **no** |

It stops working, then starts again, then stops. That's not random. `REACH` is
50, so the patch of floor where he can eat is 100 pixels wide — 50 either side
of the bread. Once one frame moves him further than that whole patch, he can
step clean over it and never once be close enough to eat. Whether he actually
does depends on exactly where his steps happen to land, which is why 150 works
and 120 doesn't.

Games really do have this bug, and it's called **tunnelling**. It's why a fast
enough bullet sometimes goes through a wall.

**2. The diagonal is faster.** Hold `right`. Then hold `right` and `up`
together. It *feels* quicker — and it is:

| holding | distance covered in one second |
| --- | --- |
| right | 244 px |
| right + up | 345 px |

That's 1.41 times as far, which is √2, and it's for the plainest possible
reason: you added `SPEED` to `x` and `SPEED` to `y` in the same frame, so he
moved `SPEED` across *and* `SPEED` down, and the actual distance from corner to
corner of that little square is longer than either side.

Almost every game you have played has had this bug at some point. Now you know
what to look for.

**3. Reach.** `REACH` is how close his middle has to get to the bread's middle.
Try `10`. Then `200`.

**4. Break the touching test on purpose.** In `is_touching`, delete the second
half so it only checks `x`:

```python
    return abs(ax - bx) < REACH
```

Now he eats bread that's in the same vertical stripe as him, however far up or
down it is. It still *works* — it's just wrong, and you have to play it for a
few seconds to notice, which is what makes this kind of bug expensive.

**5. The real one.** Put it back, then try this instead:

```python
    return ((ax - bx) ** 2 + (ay - by) ** 2) ** 0.5 < REACH
```

That's the distance formula from maths class — the length of the diagonal of a
right-angled triangle — and it is genuinely how games decide whether you got
hit.

Here's what it fixes. With `REACH = 50`:

| gap | the version you started with | the distance version | how far apart they really are |
| --- | --- | --- | --- |
| 49 across, 0 down | touching | touching | 49 px |
| 35 across, 35 down | touching | touching | 49 px |
| **49 across, 49 down** | **touching** | **not touching** | **69 px** |

The first version draws an invisible *square* around him and counts anything
inside it. The corners of a square are further away than its sides, so he can
eat bread that's 69 pixels away as long as it's diagonal. The distance version
draws a *circle* instead, and a circle is the same distance all the way round.

**6. Make it yours.** `SIZE` and `BACKGROUND`, same as lesson 1.

---

## Break it on purpose

**These four stop the program and tell you what you did:**

1. Delete `return x, y` from the bottom of `move`.
2. Put it back, then change it to `return x`.
3. Ask for `keys["Up"]` with a capital U.
4. Delete the `return` from the front of the line in `is_touching`.

Number 3 is the one worth reading carefully. `"up"` and `"Up"` are two
completely different things to Python, and it does not guess what you meant.
Every label you'll ever use — in this program and every other — has to match
exactly, character for character.

**This one says nothing at all:**

5. Set `REACH = 200` and just stand still near the middle.

No error. He eats bread from most of the way across the room without moving,
because you told him his reach was 200 pixels and he believed you. The program
is doing precisely what you asked. It's your idea of the game that's broken, and
no error message can catch that.

---

## Teacher notes

**The one concept:** the program now asks the outside world a question every
frame and behaves differently depending on the answer. Everything with a screen
works this way.

**The `y` discovery is the moment to protect.** Make her commit to a guess out
loud before running it. Getting it wrong and *seeing* it wrong in one second is
worth far more than being told, and it's the first time the computer will have
corrected her about something she was sure of.

**On `keys`.** She's using a lookup table without being told what one is called.
That's deliberate — the name and the mechanics come later, when she has a reason
to care. If she asks, "a labelled box of values" is enough for now.

**Expect these:**

- *Up and down go the wrong way.* Intended. See above.
- *Diagonal feels fast.* Some students notice unprompted, which is a very good
  sign. The fix (normalising the movement) is deliberately not in this lesson —
  noticing is the whole win here.
- *Challenge 1 (tunnelling).* Note that it does NOT happen at 60 — she has to
  push past 120 before he starts skipping over the bread, and even then it comes
  and goes depending on where his steps land. The intermittency is the valuable
  part: a bug that appears at 120, vanishes at 150 and returns at 200 is exactly
  the kind that's miserable to track down, and she gets to see why.
- *Challenge 5 (square vs circle).* The best one in the lesson if she's had
  Pythagoras in maths. "The thing you were made to memorise is how games know
  you got shot" lands hard.
- *She'll want two players.* Good. That's the next lesson, and it's the one
  where this becomes a game you can actually play with someone.

**On the sprites facing sideways when he walks vertically:** say it before she
asks, or she'll think she broke it. There are only left and right drawings.

**End of session:** screenshot into `progress/`.

---

## What next

Right now there's one of him and one of you. Next lesson there are two of each —
which sounds like it should just mean doing everything twice, and the moment you
try it you'll find out why programmers don't do things twice.
