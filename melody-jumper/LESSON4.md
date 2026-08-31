# Lesson 4 — The band

**The fundamental:** several things running at once, all measured against one
clock. And a list of dictionaries — the shape almost every real program uses to
describe "a bunch of similar things".
**Time:** ~75 min. **File:** [band.py](band.py)

---

## Run it

From the `python-games` folder:

```
./venv/bin/python melody-jumper/band.py
```

Four instruments, four balls, scrolling right to left past a line in the middle.
That line is **now**. Every ball lands on it at the same moment it makes its
sound.

- **SPACE** pauses
- **R** starts over
- **1 2 3 4** mute an instrument
- **ESC** quits

**Watch the first twenty seconds without touching anything.** It starts with one
low instrument on its own. Every time the tune comes round, another one joins.
That is the piece — Grieg wrote it to creep in and end up enormous.

---

## What's actually happening

### Three of these are playing the same tune

Look at the screen. The top three lanes have *identical shapes*, just at
different heights. That's not laziness — it's what "In the Hall of the Mountain
King" actually is. One four-bar tune, played low and quiet to start with, then
handed up the orchestra an octave at a time until everyone is playing it at
once.

The fourth lane, `pulse`, is the only one doing something different: rocking
back and forth between two notes underneath everything else. That's the left
hand of Grieg's own piano version of the piece.

### Why this couldn't just be jumper.py with more balls

In lesson 2, a platform's position came from the note before it — each gap was
worked out from how long the previous note lasted. That is completely fine for
one ball, and it falls apart the moment there are two.

Here's the actual problem. Take two instruments playing the same eight beats of
music, one as eight short notes and one as four long ones, and ask lesson 2's
code where each ends up:

| part | after 8 beats of music, x = |
| --- | --- |
| eight 1-beat notes | 1704 |
| four 2-beat notes | 852 |

Same eight beats. One ends up **twice as far along** as the other. Within
seconds one ball is off the side of the screen and the band has fallen apart.

So this program does it differently: **position comes from time.** A note that
starts on beat 12 is drawn at beat 12 — always, no matter what any other
instrument is doing. Everything lines up because everything is measured against
the same clock.

That is not a programming trick. It is how a real band stays together: nobody
follows anybody, everybody follows the count.

### Reading the screen

Each instrument gets a lane. Inside its lane, high notes sit high and low notes
sit low — same idea as lesson 2, just four of them stacked.

The **width** of a pad is how long the note lasts. Most of this tune is short
notes, so most pads are narrow bricks, with a wider one at the end of each
phrase.

The faint vertical lines are beats. The brighter ones are **bars** — every four
beats — with the chord name above. The bass sits on `Bm` for three bars and
moves to `D` for the fourth, which is why the pulse lane jumps up at the end of
every cycle.

Hollow pads are notes that are *not being played* — either an instrument hasn't
joined yet, or you've muted it. You can see what it would have played.

### A list of dictionaries

Look at `PARTS`. It's a list, and every item is a `{...}` block with the same
four labels: a `name`, a `voice`, a `color`, and a `melody`.

```python
{
    "name": "low",
    "voice": "heavy",
    "color": (176, 138, 255),
    "melody": [("B2", 0.5), ("C#3", 0.5), ...],
},
```

A **dictionary** stores things by name instead of by position. `part["voice"]`
means "the voice of this part". You don't have to remember that the voice is the
second thing — you just ask for it by name.

This is the shape you will meet over and over: a list of dictionaries, all with
the same labels, one per thing. Rows in a spreadsheet. Contacts in a phone.
Enemies in a game.

The program never mentions "low" or "pulse" anywhere in the machinery. It just
loops over `PARTS` and does the same thing to each one. **Add a fifth dictionary
and a fifth instrument appears** — no other change needed.

---

## Challenges

`is_playing` runs at the start of every bar, once per instrument. Return `True`
and it plays; return `False` and it goes quiet.

Unlike the other lessons, this function **already has real code in it** — the
staggered entrance you heard when you ran it. So the first challenge is to take
it away.

Numbers below are notes played in the first 28 seconds, which is about 16 bars.

**1. Everybody in from the start.** Delete the whole body and put:

```python
    return True
```

| part | as shipped | with `return True` |
| --- | --- | --- |
| low | 105 | 105 |
| mid | 53 | 105 |
| high | 27 | 105 |
| pulse | 49 | 65 |

Now listen. It's *worse*. Everything arrives at once, it's the same volume from
the first second to the last, and it stops being creepy. The build wasn't
decoration — it was most of the effect. Put the original code back.

**2. Drop the top line.**

```python
    return part_name != "high"
```

`high` goes to 0 notes, everything else carries on. The `"solo"` voice is the
piercing one, so this is the difference between menacing and shrieking.

**3. Every other bar.**

```python
    if part_name == "pulse":
        return bar_number % 2 == 0
    return True
```

Pulse: 65 notes → 33. `%` gives the remainder after dividing, so
`bar_number % 2 == 0` is true on bars 0, 2, 4, 6 and false on the odd ones.

**4. The drop.**

```python
    return bar_number % 8 < 6
```

Everything plays for six bars, then everything stops for two, then it all comes
back — 105 notes each becomes 79. This is the single most-used trick in modern
music and it is one line of arithmetic.

**5. Make it run.** `TEMPO` ships at `138`, which is what Grieg wrote at the
*start* of the piece. It gets faster all the way through. Try `180`. Then `220`.
Then `300`, which is past the point where you can still hear the notes as
separate things.

**6. Swap the voices.** Give `low` the `"searing"` voice. Give `high` the
`"bell"`. The notes never change and it stops being the same piece.

---

## Your turn — add a fifth instrument

Copy one of the blocks in `PARTS`, paste it at the end, and change the four
labels. Something like this, which holds long notes under everything else:

```python
    {
        "name": "drone",
        "voice": "moog",
        "color": (255, 140, 190),
        "melody": [("B1", 4), ("B1", 4), ("B1", 4), ("D2", 4)],
    },
```

Run it. A fifth lane appears, the other four shrink to make room, and key **5**
now mutes it. You didn't touch the machinery once.

Then add it to `is_playing` so it joins at some point:

```python
    if part_name == "drone":
        return bar_number >= 2
```

**Your part does not have to be the same length as the others.** The tune is 16
beats; try making yours 6. Nothing breaks — the loops just come back around at
different times, and since every part is nailed to the same clock, none of them
drifts. Loops of 32, 12 and 6 beats stay in time indefinitely.

**Notes that will fit**, because the piece is in B minor:

```
B  C#  D  E  F#  G  A
```

in any octave — `B2`, `F#3`, `D4`. Add `F` and `C` if you want the creepy sound
from bar 2 of the tune; those two are deliberately outside the key, which is the
entire reason that bar sounds wrong in a good way.

---

## Break it on purpose

**These stop the program and tell you which instrument the problem is in:**

1. Change a note in `low` to `("H4", 0.5)`.
2. Change a note in `mid` to `("C", 1)` — no octave number.
3. Give a note a length of `0`.
4. Give a part `"voice": "trumpet"`.
5. Delete the `"color"` line from one of the parts.
6. Replace a whole part's melody with `[("-", 4)]` — nothing but rests.
7. Make `is_playing` end with `return "yes"` instead of `True` or `False`.

Notice that most of those messages name the part: *"In the part 'low': I don't
understand the note 'H4'."* With one instrument you could guess where a problem
was. With five you can't, so the machinery tells you.

---

## Teacher notes

**The one concept:** independent things sharing a single source of truth. This
is the first program where "what time is it?" is answered in exactly one place
and everything else is derived from it — and it's much easier to teach because
the alternative *visibly fails*.

**Show the failure first if you have time.** Put two parts in with different
rhythms on lesson 2's layout and watch one ball leave the other behind. The
1704-vs-852 table above is that experiment as numbers.

**Challenge 1 is the important one** and it's backwards from the usual shape:
she deletes working code and the result is worse. Ask her to predict what
`return True` will do before she runs it. Almost everyone expects "fuller, so
better", and it isn't.

**On dictionaries.** Resist explaining the syntax up front. Have her add a fifth
part by copying a block first, see it work, and *then* ask what `part["voice"]`
means. The shape teaches itself faster from a working copy-paste than from a
definition.

**Startup takes about a second** here — 31 separate sounds, because it builds
one per pitch *per voice*, and four instruments across three octaves adds up.
The progress bar is there for that reason.

**Expect these:**

- *Impatience during the build.* It takes 21 seconds before all four are
  playing. That's deliberate and it's the piece, but say so, or it reads as
  broken.
- *Wanting more instruments than fit.* Five is comfortable, six is cramped. Lane
  height is the play area divided by the number of parts.
- *Notes outside B minor.* They'll sound wrong — except `F` and `C`, which sound
  wrong *on purpose* and are already in the tune. That distinction is worth
  drawing out: Grieg broke the rule deliberately, and knowing which rule he broke
  is the difference between a mistake and a choice.

**About the music.** The notes are Grieg's, taken off the score rather than
approximated — five independent published sources agree on them, including the
LilyPond source of his own piano arrangement. Bar 2 is the part everyone gets
wrong when they try to work it out by ear, so if she attempts it in `finder.py`,
expect that bar to be the hard one.

**End of session:** screenshot into `progress/`, and keep her fifth part.

---

## Where this could go next

The obvious ones, roughly in order of difficulty: percussion (a part where pitch
doesn't matter and rhythm does), a part built by `finder.py` dropped straight
in, making `TEMPO` speed up as the piece goes so it actually accelerates like the
real one, and letting `is_playing` look at what the *other* instruments are doing
rather than just the bar number.
