# Lesson 2 — Bread and jam

**The fundamental:** input — a program that *reacts* instead of one that replays.
**Time:** ~75 min. **File:** [lesson2.py](lesson2.py)

---

## Run it

```
./venv/bin/python pochita/lesson2/lesson2.py
```

Arrow keys move him (WASD works too). ESC quits.

There's a piece of bread and a jar of jam. Fetch Denji **one of each** and he
comes out and eats.

Play for a minute first. You'll get the bread. You won't get the jam, however
hard you mash the keys — the counter sits at `jam 0 / 1` and Denji never shows
up. **Work out why.** That's the lesson.

---

## What's going on

Lesson 1 ran on its own and you watched. Now the machinery asks *what are you
holding down right now?* sixty times a second and hands your code the answer.
That's the whole difference between an animation and a game.

It tells you through `keys`:

```python
keys["left"]      # True if the left arrow is down right now, otherwise False
```

Four labels — `"left"`, `"right"`, `"up"`, `"down"` — each one `True` or
`False`. The top-left of the window shows what's in it as you play.

And there are two numbers now instead of one: `x` is how far across, `y` is how
far down.

He faces sideways when he walks up or down. There are only left and right
drawings of him — most top-down games do the same, so it isn't a bug.

---

## Your turn — get the jam

The **bread** lands somewhere on the row he's standing on. The **jam** lands in
his column, directly above or below him.

Now look at `move`. There's a left and a right. There is no up and no down — and
up-or-down is the only direction the jam ever appears in.

**Add the other two**, same shape as the two already there, using `keys["up"]`
and `keys["down"]` and changing `y` instead of `x`.

Put them **above** the `return x, y` line. Anything below a `return` never runs,
and the game would behave exactly as if you'd typed nothing.

**Decide which way up is before you run it.** Say your guess out loud, then hold
the up arrow.

<br>

On a screen, `y` counts *downwards*. `y = 0` is the top row of pixels, `y = 600`
is the bottom, so up means making `y` **smaller**. Everyone gets this wrong once
and then never again.

---

## Challenges

**1. Speed.** Try `1`, then `20`, then push it past sensible. Bread collected in
fifteen seconds of running wall to wall:

| SPEED | 4 | 20 | 120 | **150** | **200** |
| --- | --- | --- | --- | --- | --- |
| bread | 4.7 | 24.2 | 118.1 | **2.8** | **1.0** |

Faster is better and better — then at 150 it falls off a cliff. Leave it running
and watch: he grabs a couple, then never gets another one. He's stuck.

`REACH` is 50, so he has to get within 50 pixels. At `SPEED = 150` he jumps 150
pixels per frame, so the spots he can *ever* stand on are a coarse grid and the
bread is sitting in a gap between them. The closest he ever gets is 56 pixels.
Six pixels short, forever.

That's a real bug with a real name — **tunnelling** — and it's why a fast enough
bullet sometimes goes through a wall. **Put `SPEED` back to 4.**

**2. The diagonal is faster.** Hold `right`, then `right` and `up` together:
about 240 px in a second against about 340. A ratio of 1.4142, which is √2,
because he moved `SPEED` across *and* `SPEED` down in the same frame and the
corner-to-corner distance is longer than either side. Most games have had this
bug at some point.

**3. Reach.** How close his middle has to get. Try `10`, then `200`, then put it
back to `50` — challenge 5 needs it there.

**4. Break the touching test.** In `is_touching`, delete the second half:

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
sixty times a second. Denji still won't come out though — he needs one of *each*,
and the other counter is stuck on zero.

**5. The real one.** Put it back, then try:

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

**6. `NEEDED = 5`.** How many of each he has to fetch before Denji appears. One
number turns a thirty-second game into a real one.

**7. `WIN_MESSAGE`.** Change what Denji says. Long ones wrap by themselves.

**8. `SIZE` and `BACKGROUND`.** Same as lesson 1.

---

## Break it on purpose

**These five stop the program and tell you what you did:**

1. Delete `return x, y` from the bottom of `move`.
2. Put it back, then change it to `return x`.
3. Ask for `keys["Up"]` with a capital U.
4. Delete the `return` from the line in `is_touching`.
5. Set `NEEDED = 0`.

Number 3 is worth reading properly. `"up"` and `"Up"` are two different things to
Python, and it will not guess what you meant.

**This one says nothing at all:**

6. Set `REACH = 200` and play. **Watch him, not the score.**

No error, and the score barely changes — what slows him down is running about,
not reaching. But look at what he's doing: he snatches things from two
body-lengths away without going near them. The program did exactly what you
asked. It's your idea of the game that's broken, and no error can catch that.

---

## Teacher notes

**The one concept:** the program asks the outside world a question every frame
and behaves differently depending on the answer.

**The jam is the assignment.** It's placed so it's provably unreachable until she
writes vertical movement — verified: with the shipped code she cannot finish the
game whatever she presses. Let her fail for a few minutes before hinting.
Working out *why* is worth more than the four lines that fix it.

**Protect the `y` guess.** Make her commit out loud before running. Getting it
wrong and seeing it wrong in one second beats being told.

**On `keys`:** she's using a lookup table without being told the word for it. If
she asks, "a labelled box of values" is enough for now.

**Expect these:**

- *Up and down backwards.* Intended.
- *Challenge 1.* The cliff is between 120 and 150, not at 60. The stall is more
  striking than the number, so leave it running. Remind her to reset `SPEED` or
  challenge 2 is invisible.
- *Challenge 4.* Ask her to predict it first. Nobody predicts "infinite jam".
- *Challenge 5.* The best one if she's had Pythagoras.
- *`NEEDED = 5`* is her first design decision rather than a bug fix — no right
  answer. Worth saying so out loud.

**End of session:** screenshot into `progress/`.

---

## What next

One of him and one of you. Next lesson there are two of each — which sounds like
doing everything twice, and the moment you try it you'll find out why programmers
don't do things twice.
