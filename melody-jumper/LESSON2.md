# Lesson 2 — Find the notes yourself

**The fundamental:** events — code that runs when something *happens*, instead
of running top to bottom. And a function that hands an answer back to you.
**Time:** ~75 min. **File:** [finder.py](finder.py)

---

## Run it

From the `python-games` folder:

```
./venv/bin/python melody-jumper/finder.py
```

Your keyboard is now a piano. Hold a key. Let go. Look at the right-hand panel.

- **ENTER** keeps the note you just played
- **SPACE** held is a silence — then ENTER keeps that too
- **BACKSPACE** throws away the last note you kept
- **Z** and **X** move down and up an octave
- **Q** holds a low drone underneath, to compare notes against
- **TAB** plays back what you've kept
- **ESC** quits

---

## What's actually happening

### Nothing is written down while you hunt

This is the whole design. Working out a song by ear is a *search*: try C — no.
D — no. E — that's it. If the tool wrote down every guess, you'd spend all your
time deleting.

So playing a note and keeping a note are two different things. Look at the two
places the program stores notes:

- `last_played` — one note. The thing you just tried. It gets thrown away the
  moment you play something else.
- `recorded` — a list. Everything you decided to keep.

Wrong guesses cost you nothing. That's not politeness, it's what makes the tool
usable.

### The program isn't running in order any more

Lesson 1 ran top to bottom, sixty times a second, and you could follow along.
This one mostly sits there doing nothing until *you* do something. Then a chunk
of code runs, and it goes back to waiting.

Those somethings are called **events**. This program cares about two:

| Event | When | What it does |
| --- | --- | --- |
| `KEYDOWN` | the moment a key goes down | start the sound, write down the time |
| `KEYUP` | the moment it comes back up | stop the sound, work out how long you held it |

You can *hear* the difference. The note starts when the key goes down and stops
when it comes up. Two separate moments, two separate pieces of code. Nothing
about "how long you held it" exists until the key comes back up — that number is
made by subtracting one moment from the other.

### Rounding off

Nobody holds a key for exactly one beat. Hold one down and watch the panel: the
raw number jitters (`0.87 beats`, `0.91 beats`) while the rounded one sits
still at `1`.

That's **quantizing** — snapping a messy measurement to the nearest tidy value.
Every music program you have ever used does this, and it is the only reason
anything you record lines up.

---

## How to actually work out a song

The order below is what musicians actually do. Doing it out of order is what
makes it feel impossible.

**1. Find the home note first.** Hum the song and let it end. That last note,
the one that feels finished, is home. Hunt for *that* note before any other.
Then set `DRONE_NOTE` to it and press **Q** — now it's playing underneath, and
every other note either fits against it or clashes. Judging "does this fit?" is
far easier than "what note is this?"

**2. Do the rhythm before the pitch.** Tap the tune on the desk. Which notes are
long, which are short? Get that in your head before you hunt for a single pitch.
Trying to solve rhythm and pitch at the same time is the thing that makes people
give up.

**3. Hum it, then hunt for it.** Sing the note out loud first. *Then* go looking
for it. If you skip the humming and just mash keys until something matches, you
haven't used your ear at all — you've used the computer's.

**4. Work in short phrases.** Six to ten notes. Press **TAB** every couple of
notes to hear what you have. Catching a wrong note when there are three is easy.
Catching it when there are twenty is not.

**5. Looking the notes up is allowed.** Find a piano tutorial for the song on
YouTube and read the notes off it. This is what real musicians do constantly.
Use your ear for the rhythm and your eyes for the pitches if that's what gets it
done — it still counts.

**If the whole thing sounds right but too high or too low,** you got the tune
right and the octave wrong. That's the single most common mistake. Press Z, and
do it again one octave down.

---

## Challenges

Find `on_note_played` at the top of the file. It runs once, each time you press
ENTER, and whatever it hands back is what goes into your song.

**1. Every note the same length.**

```python
    return (note_name, 1)
```

Play notes of wildly different lengths and keep them. They all come out as `1`.
The length you held is still measured and still passed in — this function just
ignores it and hands back something else.

**2. Keep nothing.**

```python
    return None
```

Play a note. Press ENTER. Watch the status line: *"on_note_played() returned
None — D4 not kept"*. Nothing is broken. `None` is Python's way of saying "no
answer", and the machinery is written to take that as "don't keep this one".

**3. Half speed.**

```python
    return (note_name, held_beats * 2)
```

Every note lasts twice as long. Record a few and press TAB.

**4. Ignore quick taps.** This one is genuinely useful:

```python
    if held_beats < 1:
        return None
    return (note_name, held_beats)
```

Now short taps are thrown away and only notes you deliberately held get kept.
Two lines, and the tool behaves differently.

**5. Change the voice.** `VOICE = "bell"`. Then `"solo"`. Then `"searing"`.
Hunting for notes is much easier with a clean sound than a distorted one — but
`"solo"` is more fun.

---

## Your turn — get eight notes

Pick a song you can already hum. Work out **eight notes of it**. Not the whole
song — eight notes.

That's the assignment, and finishing it means the tool worked.

When you have them, quit with ESC. Two things happen:

1. The notes are already saved into `my_song.py`, right next to `jumper.py`
2. The same list gets printed in the terminal, ready to paste anywhere

Now run the jumper:

```
./venv/bin/python melody-jumper/jumper.py
```

It plays **your** song. The platforms are the shape of the tune you just worked
out by ear. The title in the corner says `my_song.py` so you know where it came
from.

To go back to the built-in song, delete `my_song.py`, or set
`USE_MY_SONG = False` in `jumper.py`.

---

## Break it on purpose

**These stop the program and tell you what you did:**

1. Make `on_note_played` end with `return "hello"`.
2. Make it return three things: `return (note_name, held_beats, 5)`.
3. Make it return a length of zero: `return (note_name, 0)`.
4. Make it return words for the length: `return (note_name, "long")`.
5. Set `VOICE = "trumpet"`.
6. Set `DRONE_NOTE = "H2"`.

Every one of those tells you which line to look at. That is not normal — most
programs would give you a screenful of red text about something else entirely.
Somebody had to sit down and write each of those messages, guessing what you
were likely to get wrong.

**This one says nothing at all:**

7. Set `TEMPO = 300` and record a few notes at your normal speed.

No error, but look at what comes out. At 300 bpm a beat is only a fifth of a
second, so everything you play measures as far more beats than you meant:

| you hold for | at 92 bpm | at 300 bpm |
| --- | --- | --- |
| 0.3s | 0.5 | 1.5 |
| 0.5s | 1 | 2.5 |
| 0.65s | 1 | 3 |
| 0.8s | 1 | 4 |
| 1.3s | 2 | 4 |
| 2.0s | 3 | 4 |

Short notes get stretched. And anything you hold for longer than about
0.8 seconds comes out as `4` — because the machinery quietly refuses to record
anything longer than four beats, so all your long notes collapse into the same
value and stop being different from each other.

Nothing warned you. **Set `TEMPO` roughly to the speed of your song before you
start recording**, not after.

---

## Teacher notes

**The one concept:** events. Code that waits for something to happen instead of
running straight through. Everything with a screen works this way, and this is
the first lesson where the program is idle until she acts.

**The second concept, quietly:** a function that *returns* a value rather than
one that changes something. `on_note_played` hands an answer back; the machinery
decides what to do with it. This matters because the next step — her writing a
call site herself — is much easier from here.

**No new setup.** Same venv, same one dependency. All three programs in this
folder share `tones.py`, which is the first time she'll see one file importing
another.

**Expect these:**

- *Octave errors.* Very common and not a sign of a bad ear — low fundamentals
  genuinely fool everyone. Z and X fix it in one keypress.
- *Wanting to record every guess.* If she asks "why didn't that get saved?",
  that's the design working. Point at `last_played` and `recorded` side by side.
- *Rhythm before pitch.* If she's struggling, it's almost always because she's
  solving both at once. Have her tap the rhythm on the desk first.
- *The `TEMPO = 300` clamp.* Worth doing on purpose. It is the nastiest kind of
  bug: the program keeps working, gives you something wrong, and never says a
  word about it.
- *Budget the last 15 minutes for running the jumper.* The payoff of this lesson
  is watching the ball jump her own song. If she leaves before that happens, the
  session reads as busywork.

**Set the bar at eight notes, not at a finished song.** And say out loud that
looking pitches up is what real people do — otherwise reaching for help reads as
failure to her, and she'll stop.

**On choosing her song.** The built-in tune in `jumper.py` and `band.py` is
Grieg's "In the Hall of the Mountain King", because it's out of copyright and its
notes are therefore actually published — five independent sources agree on them.
Almost no current song is like that. Pop melodies are rarely written down
anywhere you can check, which is the real reason this lesson exists: if she wants
a song from this decade in her program, working it out by ear is not a shortcut,
it's the only route.

Worth saying out loud to her: transcribing a song for your own learning is
completely normal practice, and publishing the result is a different question.
That is a genuinely interesting ten minutes of conversation rather than a
warning.

If she picks something with an awkward range, the octave keys (Z and X) matter
more than usual — start by finding the *lowest* note in her phrase and putting
that on the left of the keyboard.

**End of session:** screenshot into `progress/`, and keep `my_song.py`.

---

## Next lesson

[Lesson 3 — The band](LESSON3.md). One ball playing one tune becomes four
instruments playing at once, which turns out to break the way lesson 1 placed
its platforms — and fixing it is the lesson.
