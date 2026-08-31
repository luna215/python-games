# Lesson 1 — The ball plays the song

**The fundamental:** a list of data can *be* the program. Change the list, and
everything the program does changes with it.
**Time:** ~75 min. **File:** [jumper.py](jumper.py)

---

## Run it

From the `python-games` folder:

```
./venv/bin/python melody-jumper/jumper.py
```

A window opens. A ball jumps from platform to platform on its own, and plays a
note every time it lands.

- **SPACE** pauses it
- **R** starts the song over
- **ESC** quits

---

## What's actually happening

Nobody placed those platforms. Look at the top of `jumper.py`:

```python
MELODY = [
    ("B3", 0.5), ("C#4", 0.5), ("D4", 0.5), ("E4", 0.5), ("F#4", 0.5), ...
    ("F4", 0.5), ("C#4", 0.5), ("F4", 1),   ("E4", 0.5), ("C4", 0.5),  ...
    ...
]
```

That's the whole song, and it is also the whole level. Each line becomes one
platform:

- the **note name** decides how high up the screen the platform floats
- the **number** is how many beats the note lasts, which decides how long the
  ball sits there before it jumps again

So the shape you see on screen *is* the shape of the melody. When the tune goes
up, the platforms go up. Pause it with SPACE and look — you can read the song off
the screen without hearing a thing.

There is no sound file anywhere in this folder. The computer builds every note
from scratch when the program starts, by working out tens of thousands of numbers
that describe how fast the air should shake. That happens in `tones.py`, a
separate file this one borrows from — which is what the line `import tones` at
the top is doing.

The tune it comes with is **"In the Hall of the Mountain King"**, written by
Edvard Grieg in 1875 for a play called *Peer Gynt*. You have heard it. It's the
creeping, speeding-up one that gets used every time something is sneaking up on
somebody.

Grieg died in 1907, so nobody owns this music any more — which means the notes in
`MELODY` are the real ones off the score, not an imitation. Four bars, in B minor,
at the tempo Grieg wrote on it: 138 beats per minute.

**Look at bar 2** — the second line of `MELODY`. Every other bar uses notes from
B minor. That one uses `F` and `C`, which are not in the key at all, and that is
exactly why the piece sounds creepy. It's the same three-note shape played twice,
the second time one semitone lower. Grieg wrote that `F` as "E sharp", which is
the same key on a piano and tells a musician something about where the note is
going.

### Reading a note name

A note name is a **letter**, then an optional `#` or `b`, then an **octave
number**.

| You write | It means |
| --- | --- |
| `C4` | middle C |
| `C5` | one octave higher — same note, but higher |
| `C3` | one octave lower |
| `F#4` | F sharp, the black key just above F |
| `Bb4` | B flat, the black key just below B |
| `-` | a rest. The ball still lands, but no sound comes out. |

The rests are the hollow platforms.

---

## Challenges

**1. Flatten it.** Find `platform_height` and replace its last two lines with:

```python
    return 0.5
```

Every platform lands at the same height and the ball rolls along a flat road.
The song sounds exactly the same. **The sound and the picture came from the same
list, but nothing forces them to agree** — you just chose to throw the pitch
information away.

**2. Upside down.**

```python
    return 1 - (note - lowest) / span
```

Now high notes sink and low notes climb. Confusing to watch, which is the point:
your brain already expected higher notes to be higher up, and nobody taught it
that.

**3. Only the peaks.**

```python
    return ((note - lowest) / span) ** 3
```

The highest note stays right where it was. Everything else drops toward the
floor. Cubing a number between 0 and 1 makes it much smaller unless it's already
close to 1.

Put the original two lines back before moving on.

**4. Tempo.** `TEMPO` is beats per minute. It ships at `138`, which is what's
printed on Grieg's score. Try `46`, then `220`.

Two separate things change, and it's worth telling them apart.

First, **the gaps between platforms get smaller as the tempo rises**, because
there's less time to travel:

| TEMPO | gap after a half-beat note |
| --- | --- |
| 46 | 213 px |
| 107 | 143 px |
| 160 | 119 px |

Second, at any one tempo, **longer notes get wider gaps**. At the shipped 138:

| note length | gap |
| --- | --- |
| half a beat | 127 px |
| a whole beat | 183 px |

So the rhythm of the tune is visible in the spacing without hearing anything —
the six quick steps at the start of each bar are evenly close together, then
there's a wider jump for the long note. Pause with SPACE and read it off the
screen.

The real piece speeds up continuously from beginning to end. `220` gets you
somewhere near the ending.

**5. Gravity, and a surprise.** `GRAVITY` is in the machinery section.

**Set `TEMPO = 46` first.** Then try `GRAVITY` at `900`, then `3200`. You need
the slow tempo for this one, and the reason why is the whole point — come back to
it in a moment.

You would expect more gravity to mean flatter jumps. It does the opposite:

| GRAVITY | highest point at TEMPO 46 |
| --- | --- |
| 900 | y = 237 |
| 1900 (shipped) | y = 200 |
| 3200 | y = 151 |

Smaller y is higher up the screen, so more gravity really does throw the ball
*higher*.

Here's why. The ball **must** land exactly when the next note is due. So when you
crank up gravity, the program has to throw it much harder to keep it in the air
that long — and throwing it harder sends it higher. The landing time is fixed;
the height is whatever falls out of that.

**Now put `TEMPO` back to 138 and try the same thing.** Almost nothing happens.

That's the second half of the lesson. How high the ball goes depends on how long
it's in the air, *squared* — and at 138 bpm these notes are so short (a fifth of
a second) that the jumps are only a few pixels high no matter what gravity says.
Two settings you'd think were unrelated turn out to control each other.

Here's why. The ball **must** land exactly when the next note is due, no matter
what. So when you crank up gravity, the program has to throw the ball much harder
to keep it in the air that long, and throwing it harder sends it higher. The
landing time is fixed and the height is whatever falls out of that.

**6. The sound itself.** `VOICE` picks how the notes are made. Try all seven:

| | |
| --- | --- |
| `bell` | clean and soft |
| `pluck` | short and woody |
| `lead` | detuned and driven |
| `heavy` | the same, plus an octave underneath |
| `searing` | a square wave, distorted hard |
| `moog` | three detuned saws that swell in, with an echo — the one it ships with |
| `solo` | distorted, and it *slides* up into every note |

Same notes, same platforms, completely different song. Listen to `bell` and then
`solo` back to back — that difference is nothing but arithmetic, and it's all in
`tones.py` if you want to look.

**7. Colours.** `BALL_COLOR`, `PLATFORM_COLOR`, `ACTIVE_COLOR`. Three numbers
each: red, green, blue, `0` to `255`.

---

## Your turn — put a real song in there

This is the actual assignment. Pick a song you like and type its melody into
`MELODY`.

You do not need to read music. Here's the method that works:

1. Find the song's notes. A piano app on your phone, or an online keyboard, or
   [onlinesequencer.net](https://onlinesequencer.net). Play notes until one
   matches the first note of the tune you're humming.
2. Write it down as a name and a length. `("D4", 1)` — one beat.
3. Do the next note. Then the next. Four or five notes is already enough to
   recognise.
4. Run it after every couple of notes. Wrong ones are obvious immediately, and
   it's much easier to fix two notes than twenty.

**Things worth knowing while you do it:**

- If the whole thing sounds too high or too low, change every octave number at
  once — all the `4`s to `3`s. The tune stays the same, it just moves down.
- If it sounds right but feels wrong, your lengths are off, not your notes.
  Rhythm is the half people get wrong.
- Set `SONG_TITLE` to the name of your song so it shows in the corner.

Melodies loop forever, so a good one is about 8 to 20 notes.

**There's an easier way to do this, and it's the next lesson.**
[finder.py](finder.py) turns your keyboard into a piano so you can hunt for the
notes by ear and have it write the list for you. If typing note names into a file
is annoying you right now, that annoyance is the reason lesson 2 exists — go and
do [Lesson 2](LESSON2.md), then come back here and run this again.

---

## Break it on purpose

**These stop the program and tell you what you did:**

1. Change a note to `("H4", 1)`. There is no note called H.
2. Change a note to `("C", 1)` — the letter with no octave number.
3. Give a note a length of `-1`.
4. Delete every line of `MELODY` except one.
5. Make `platform_height` end with `return "high"` instead of a number.

Read each message. They were written for you, on purpose. Most of the time a
program that breaks gives you thirty lines of red text about something that
isn't the problem.

**This one says nothing at all:**

6. Make `platform_height` end with `return 5`.

No error. The platforms all jump to the top of the screen and stay there. The
machinery quietly squashes anything above 1 back down to 1, because a platform
above the top of the window is no platform at all.

That's a decision somebody made, buried in code you didn't write, that changes
what you see and never mentions it. Software is full of these.

---

## Teacher notes

**The one concept:** the program's behaviour lives in a list of data, not in the
instructions. Changing one line of `MELODY` moves a platform, changes a landing
time, changes a jump arc, and changes a sound — four things at once, from one
edit.

**Setup** is the four commands in the [README](../README.md), and nothing beyond
them. The sound is generated in Python with the standard library, so there's
nothing to download and it works with no internet.

**Startup takes about a fifth of a second** for this song — you may not even see
the progress bar. It builds one sound per pitch, and how long each takes depends
on the voice (`heavy` and `moog` are the slow ones) and on the song's longest
note, since that sets how long the tones need to be.

**Expect these:**

- *Challenge 1 (the flat road).* Worth pausing on. The picture and the sound come
  from one list, and separating them makes it obvious that neither one is "the
  real song".
- *Challenge 5 (gravity backwards).* Genuinely counterintuitive, and the
  explanation is the good part: the constraint is the landing time, so height is
  the thing that has to give. If they predict "flatter" and get "higher", that
  is the lesson working. It only shows at a slow TEMPO — at the shipped 138 the
  notes last a fifth of a second and the arcs are a few pixels high whatever
  gravity is set to. Make them do it both ways; "why did it stop working?" is
  the better half of the question.
- *Writing their own melody.* This is where the time goes and where the interest
  is. Expect the rhythm to be wrong before the notes are. Getting four correct
  notes of a song they actually like beats twenty notes of one they don't.
- *"Can I use a real song?"* Yes — typing in a melody by ear for yourself is
  fine, and it is by far the best way to spend this lesson. Note names in a text
  file, not an audio file.
- *Where the tune came from.* The notes in `MELODY` are Grieg's, read off the
  score, not an approximation — the piece is out of copyright. If she asks why
  this one and not something current: current songs mostly don't have their
  melodies published anywhere, which is exactly the gap lesson 2 fills.

**If they ask how the sound is made:** every note is a list of about 60,000
numbers, one every 1/44100th of a second, describing where a speaker cone should
be. `tones.py` draws one cycle of a wave, then walks around it at the right
speed. The `VOICES` table near the top is the good part to show them — each voice
is the same machine with different dials, and the comment block above it says
what every dial does. Change one number and re-run.

**End of session:** screenshot into `progress/`, and keep their melody.

---

## Next lesson

[Lesson 2 — Find the notes yourself](LESSON2.md). Typing note names into a list
is the slow way. Next lesson builds the tool that listens instead: a keyboard you
can hunt around on until a note matches the song in your head, which then writes
this list for you.
