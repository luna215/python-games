# Lesson 2 — Bread and jam

**The fundamental:** input. A program that *reacts* instead of one that replays.
And a second number, `y`, which turns out not to work the way you'd expect.
**Time:** ~75 min. **File:** [lesson2.py](lesson2.py)

---

## Run it

```
./venv/bin/python pochita/lesson2/lesson2.py
```

**Arrow keys** move him — WASD works too. **ESC** quits. On the finish screen,
click **Play again**, or press ENTER or SPACE.

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

Now the machinery asks a question sixty times a second — *what are you holding
down right now?* — and hands your code the answer. That's the entire difference
between an animation and a game, and it's why every game ever made has a loop
like this one at its heart.

### The camera moved

The ground line is gone. Lesson 1 watched him from the side, so there was a line
for him to walk along. This one looks straight down at him from above,
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

He's drawn out of plain shapes in the machinery — circles, rectangles and
triangles, and that's all. No picture files anywhere. Worth knowing, because it
means you could draw anything the same way.

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

Put them **above** the `return x, y` line. `return` means "the function stops
here and hands this back", so anything you type underneath it never runs at all —
and the game would behave exactly as if you hadn't typed anything, which is a
miserable thing to debug.

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

Here's how much bread he collects in fifteen seconds of running wall to wall,
averaged over ten random layouts:

| SPEED | bread collected |
| --- | --- |
| 4 | 4.7 |
| 20 | 24.2 |
| 60 | 71.2 |
| 100 | 108.6 |
| 120 | 118.1 |
| **150** | **2.8** |
| **200** | **1.0** |

Faster is better, and better, and better — and then at 150 it doesn't just get a
bit worse, it **falls off a cliff**. From 118 to under 3.

And it's worse than the number makes it look. Run it at 150 and watch: he grabs a
few pieces in the first half-second and then **never gets another one**, for as
long as you leave it going. He isn't unlucky. He's stuck.

`REACH` is 50, so he has to get within 50 pixels. At `SPEED = 150` he moves 150
pixels between one frame and the next, so the places he can *ever* stand have
become a coarse grid with big gaps in it — and the bread is sitting in a gap.
Measured over thirty seconds: the closest he ever gets to that piece of bread is
**56 pixels**. Six pixels too far, forever.

Games really do have this bug, and it's called **tunnelling**. It's why a fast
enough bullet sometimes goes straight through a wall.

**Put `SPEED` back to 4 before the next one** — it needs the ordinary speed.

**2. The diagonal is faster.** Hold `right`. Then hold `right` and `up`
together. It *feels* quicker — and it is:

| holding | distance covered in one second |
| --- | --- |
| right | about 240 px |
| right + up | about 340 px |

The exact distances wobble a little depending on how many frames your computer
fits into a second, but the *ratio* doesn't: it is 1.4142, every time. That's √2,
and it's for the plainest possible
reason: you added `SPEED` to `x` and `SPEED` to `y` in the same frame, so he
moved `SPEED` across *and* `SPEED` down, and the actual distance from corner to
corner of that little square is longer than either side.

Almost every game you have played has had this bug at some point. Now you know
what to look for.

**3. Reach.** `REACH` is how close his middle has to get. Try `10`. Then `200`.
Then put it back to `50` — challenge 5 below only makes sense at 50.

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

That's the distance formula from maths class — the length of the hypotenuse of a
right-angled triangle — and it is genuinely how games decide whether you got hit.

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
change — nothing else in the file needs touching. The counter in the corner now
starts at `bread 0 / 5` and keeps score as you go.

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

6. Set `REACH = 200` and play for a bit. **Watch him, not the score.**

No error, and the score barely moves — about 5 pieces in fifteen seconds either
way, because what slows him down is running about, not reaching. But look at what
he's actually doing: he now snatches things from two body-lengths away, without
ever going near them. Food leaps into him.

The program is doing precisely what you asked. It's your idea of the game that's
broken, and no error message will ever catch that — you have to *look*.

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
- *Challenge 1 (tunnelling).* It does **not** happen at 60 or even 120 — those
  are fine and get faster and faster. The cliff is between 120 and 150, and it is
  a cliff: 118 pieces down to under 3. Have her leave it running at 150 and watch
  him fail to collect anything for thirty seconds; the stall is far more striking
  than the number. Measured: after the first half-second he never again gets
  closer than 56 px to the bread, needing 50. Six pixels short, permanently.
  Remind her to put SPEED back to 4 — challenge 2 is invisible at 150 because
  he hits the walls within a couple of frames.
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
