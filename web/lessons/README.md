# What a lesson is

Each folder in here is one lesson, and it holds exactly three files:

```
starter.py    the code the editor starts with. Keep it SHORT — the point is
              that a student can see the whole thing at once and not feel
              they're staring at a program. Explanation belongs in lesson.md,
              not in comments here. Lesson 1 is thirteen lines.

lesson.md     the instructions panel: a summary, then one step at a time.
              The challenges and "break it on purpose" carry over from the
              LESSON*.md card; the terminal instructions and the teacher
              notes don't.

lesson.js     THE MACHINERY, in JavaScript.
```

`app.js` finds a lesson by its id, from `?lesson=<id>` in the URL, and lists it
from the `LESSONS` array at the top of that file. Add a folder, add a line
there.

## How lesson.md is laid out

One file, split into a summary and then one chunk per step by `<!-- step -->`
on a line of its own. It's an HTML comment, so the file still reads as an
ordinary document if you open it on GitHub.

```markdown
# Lesson title

Two or three lines on what they'll be doing. This sits pinned at the top of
the panel, and folds away once they're past the first step.

<!-- step -->

## First step

...

<!-- step -->

## Second step
```

The `## ` heading is the step's name — it's what the **All steps** view lists,
and clicking it there jumps back into the stepped view.

Keep each step to one thing. The panel is a quarter of the screen and about
forty characters across; anything longer than a few short paragraphs will need
scrolling, which is exactly the wall of text the stepping is there to avoid.

A step that asks them to change something should say to **Run it** — the game
only appears when they press that, and it replaces the code while it plays.

## What lesson.js has to export

One default object:

```js
export default {
  meta: {
    id, width, height,     // the logical canvas, in the game's own pixels
    consts: [...],         // names read out of the student's code on each Run
    checks: [...],         // which of pyrunner.py's validators to run
    needs: [...],          // functions that have to exist
    note: "...",           // the grey line next to "YOUR CODE"
  },

  async preload(),         // load artwork. Runs once, before Python is ready.
  configure(consts),       // a fresh set of constants. Runs on every Run.
  reset(),                 // put the game back to the start.
  step(now, input, py),    // advance one 60Hz tick. May throw.
  draw(ctx, now, input),   // paint one frame.
  pointer(kind, pos),      // optional — "move" or "down", in game coordinates.
};
```

`step` is where you call the student's code, through `py.move1(...)`,
`py.move2(...)` or `py.touching(...)`. If it throws, the shell stops the loop,
leaves the last frame on screen and shows the message; you don't need to catch
anything yourself.

## The rule worth keeping

A lesson.js is a port of the machinery in the matching `.py` file, and the
lesson cards are full of specific numbers measured against that machinery —
"bread collected in fifteen seconds", "the closest he ever gets is 56 pixels".
Those numbers have to stay true here, which is why `engine.js` runs a fixed
60Hz step instead of trusting the display's refresh rate.

Port behaviour, not just appearance.
