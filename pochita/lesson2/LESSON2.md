# Lesson 2 — Bread and jam

**The fundamental:** input. A program that *reacts* instead of one that replays.
And a second number, `y`, which turns out not to work the way you'd expect.
**Time:** ~75 min. **File:** [lesson2.py](lesson2.py)

---

## Run it

```
./venv/bin/python pochita/lesson2/lesson2.py
```

**Arrow keys** move him. **ESC** quits. On the finish screen, click
**Play again** — or press ENTER or SPACE.

There's a piece of bread and a jar of jam. Fetch Denji **one of each** and he
comes out and eats.

Play for a minute before you read any further.

You'll get the bread easily. You will not get the jam, no matter how hard you
mash the keys — the counter in the corner sits there saying `jam 0 / 1`, and
Denji never appears.

**Work out why.** That's the lesson, and everything below is here to help once
you've had a proper go at it yourself.

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

The floor is gone. Lesson 1 watched him from the side, so there was a ground
line and he walked along it. This one looks straight down at him from above,
which is why there's a whole room to move around in instead of one line.

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

Look at the top-left of the window while you play. It shows you exactly what's in
`keys` at that moment.

### Two numbers now

Lesson 1 had `x`: how far across. This has `x` **and** `y`: how far across, and
how far down. Together they say exactly where the middle of him is, and the
corner of the window shows you both while you move.

### Denji only comes out for both

Bread on its own isn't a meal. Denji wants bread **and** jam, so the game waits
until Pochita has fetched one of each before anything happens — which is why you
can run around collecting bread all afternoon and get nowhere.

When he finally does turn up, he arrives on a see-through sheet laid over the
game. You can still see the room faintly behind him, because he's *on top of*
the game rather than replacing it.

He's drawn out of plain shapes in the machinery — some circles, a couple of
rectangles and five triangles for the hair. No picture files at all. Worth
knowing, because it means you could draw anything the same way.

---

## Your turn — get the jam

Look at where the two things appear.

The **bread** always turns up somewhere along the row Pochita is standing on. It
never appears above or below him, only off to one side. It's also drawn wide.

The **jam** always turns up somewhere in the column he's standing in — directly
above or directly below. It's drawn tall.

Now look at `move`. Two of the four directions are written:

```python
    if keys["left"]:
        x = x - SPEED

    if keys["right"]:
        x = x + SPEED
```

There is no up. There is no down. He physically cannot travel in the only
direction the jam ever appears in, which is why you've been failing to reach it.

**Add the other two.** Same shape as the two above, using `keys["up"]` and
`keys["down"]`, and changing `y` instead of `x`.

**Before you run it, decide which way up is.** Say your guess out loud. Then run
it and hold the up arrow.

<br>

**If he went the wrong way, you are in good company.** On a screen, `y` counts
*downwards* from the top. `y = 0` is the very top row of pixels and `y = 600` is
the bottom. So going up means making `y` **smaller** — subtracting, not adding.

The reason is history: the first screens drew the picture one line at a time,
starting at the top and sweeping down, and the numbering followed the sweep.
Every screen since has kept it, so the graph paper from maths class is upside
down here. This trips up absolutely everyone once, and then never again.

Now go and get the jam, and meet Denji.

---

## Challenges

**1. Speed, and running straight past things.** Try `SPEED = 1`. Then `20`. Then
push it much further than seems sensible.

Here's how much bread he manages to collect in fifteen seconds of sweeping back
and forth, averaged over ten different random layouts:

| SPEED | bread collected |
| --- | --- |
| 4 | 0.8 |
| 20 | 6.2 |
| 100 | 6.3 |
| 120 | 5.9 |
| **150** | **3.0** |
| **200** | **1.0** |

It climbs, levels off, and then *falls apart*. The first bit is obvious — a
faster Pochita covers more ground. The collapse is the interesting part, and it
isn't because he's too fast to steer.

`REACH` is 50, so the patch of floor where he can eat the bread is 100 pixels
wide, 50 either side of it. At `SPEED = 200` he crosses 200 pixels between one
frame and the next. He can be well to the left of the bread, and then next frame
be well to the right of it, without ever having been close enough to eat it. He
jumps straight over the whole window.

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

**3. Reach.** `REACH` is how close his middle has to get. Try `10`. Then `200`.

**4. Break the touching test, and watch him cheat.** In `is_touching`, delete the
second half so it only checks `x`:

```python
    return abs(ax - bx) < REACH
```

Now **stand completely still and don't touch the keyboard.** Watch the counter
in the corner. Ten seconds later:

| `is_touching` checks | bread | jam |
| --- | --- | --- |
| both x and y (as shipped) | 0 | 0 |
| only `x` | 0 | **601** |
| only `y` | **601** | 0 |

It reads `jam 601 / 1`. Six hundred jars, without moving a muscle.

The jam is *always* in his column, so if you stop checking how far apart they are
vertically, he's touching it the instant it appears — and the instant the next
one appears, and the next, sixty times a second. Checking only `y` does exactly
the same thing to the bread, for the same reason in the other direction.

Notice Denji still doesn't appear. He needs one of *each*, and the other counter
is stuck on zero — so the bug hands you infinite jam and still no dinner.

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
inside it. The corners of a square are further from the middle than its sides
are, so he can eat something 69 pixels away as long as it's diagonal. The
distance version draws a *circle* instead, and a circle is the same distance all
the way round.

**6. Make him work for it.** `NEEDED` is how many of each Pochita has to fetch
before Denji appears. It ships at `1`. Try `5`.

That one number turns a thirty-second game into a real one, and it's the whole
change — nothing else in the file needs touching. Notice the counter in the
corner starts reading `bread 2 / 5` and keeps track for you.

**7. Change what Denji says.** `WIN_MESSAGE`, at the top. Put anything you like
in it. If you write something long it wraps onto more lines by itself, and the
picture and the button move down to make room — try a really long one and watch
them shuffle.

**8. Make it yours.** `SIZE` and `BACKGROUND`, same as lesson 1.

---

## Break it on purpose

**These five stop the program and tell you what you did:**

1. Delete `return x, y` from the bottom of `move`.
2. Put it back, then change it to `return x`.
3. Ask for `keys["Up"]` with a capital U.
4. Delete the `return` from the front of the line in `is_touching`.
5. Set `NEEDED = 0`.

Number 3 is the one worth reading carefully. `"up"` and `"Up"` are two
completely different things to Python, and it does not guess what you meant.
Every label you'll ever use — in this program and every other — has to match
exactly, character for character.

Number 5 is a small mercy rather than a rule. If Denji needs zero of each, he'd
turn up before you'd done anything — and then "Play again" would just hand you the
same screen forever, with no way back to the game. Somebody thought about that
happening to you and wrote a sentence instead.

**This one says nothing at all:**

6. Set `REACH = 200` and stand near the middle of the room.

No error. He eats things from most of the way across the floor without moving,
because you told him his reach was 200 pixels and he believed you. The program
is doing precisely what you asked. It's your idea of the game that's broken, and
no error message will ever catch that.

---

## Teacher notes

**The one concept:** the program now asks the outside world a question every
frame and behaves differently depending on the answer. Everything with a screen
works this way.

**The jam is the assignment, and the win screen is the payoff.** The jam is
placed so that it is provably unreachable until she writes vertical movement —
she can mash every key on the keyboard and `jam` stays at 0, so Denji never
appears at all. Verified both ways: with the shipped code she cannot reach the
end of the game no matter what she presses.

Let her fail at it for a few minutes before offering the hint. The moment where
she works out *why* she can't reach it is worth more than the four lines that fix
it, and the message with her name in it is the reward for getting there.

**The `y` discovery is the other moment to protect.** Make her commit to a guess
out loud before running it. Getting it wrong and *seeing* it wrong in one second
beats being told, and it's the first time the computer will have corrected her
about something she was sure of.

**On `keys`.** She's using a lookup table without being told what one is called.
That's deliberate — the name and the mechanics come later, when she has a reason
to care. If she asks, "a labelled box of values" is enough for now.

**Expect these:**

- *Up and down go the wrong way.* Intended. See above.
- *Diagonal feels fast.* Some students notice unprompted, which is a very good
  sign. The fix is deliberately not in this lesson — noticing is the win.
- *Challenge 1 (tunnelling).* Note it does **not** happen at 60, or even at 120 —
  she has to push to 150 or 200 before he starts skipping over things, and even
  then it's a matter of where his steps land rather than a clean on/off. The
  raggedness is the valuable part: bugs that only sometimes happen are the
  expensive kind.
- *Challenge 4 (601 jars while standing still).* The funniest one and the one
  that best shows why both halves of the test matter. Ask her to predict what
  will happen before she runs it — almost nobody predicts "infinite jam".
- *Challenge 5 (square vs circle).* The best one if she's had Pythagoras. "The
  thing you were made to memorise is how games know you got shot" lands hard.
- *She'll want two players.* Good. That's the next lesson.
- *`NEEDED = 5` is the first time she'll have made a design decision* rather than
  fixed a bug — the game is genuinely better or worse depending on the number,
  and there's no right answer. Worth naming that out loud when it happens.

**On the sprites facing sideways when he walks vertically:** say it before she
asks, or she'll think she broke it. There are only left and right drawings.

**End of session:** screenshot into `progress/`.

---

## What next

Right now there's one of him and one of you. Next lesson there are two of each —
which sounds like it should just mean doing everything twice, and the moment you
try it you'll find out why programmers don't do things twice.
