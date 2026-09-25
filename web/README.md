# The browser tutorials

Same lessons as the `.py` files. The left column tells them what to do — a
summary, then one step at a time. The right half shows one thing at a time:
the code they're writing, or, once they press **Run it**, the game it makes.
No install, no Terminal, no saving a file.

Live at **https://luna215.github.io/python-games/**

---

## Running it locally

There is no build step. Any static server will do:

```
python3 -m http.server 8777
```

Then open <http://127.0.0.1:8777/web/>. Opening `index.html` straight off disk
will *not* work — the lessons are ES modules and the browser blocks those on
`file://`.

Edit a file, reload the page. That's the whole loop.

---

## Deploying

Settings → Pages → **deploy from branch `main`, folder `/ (root)`**. Nothing
else. There is no workflow file because there is nothing to build, and no
`package.json` because everything comes from a CDN.

Two files at the repo root exist only for this:

- `.nojekyll` — stops GitHub running Jekyll over a repo that isn't a Jekyll site
- `index.html` — redirects the bare Pages URL to `web/`

Serving from the root is also what lets the lessons reach `pochita/sprites/`
directly, so the artwork isn't duplicated.

---

## How it fits together

```
index.html     the shell: header, instructions, and the code/game half
app.js         boots everything; owns the stepper, the editor, and the
               swap between code and game
app.css        the two columns, the stepper, and the two right-hand modes
engine.js      canvas helpers — sprites, shapes, text, input, the 60Hz loop
pyrunner.js    starts Pyodide, and turns Python errors into something showable
pyrunner.py    runs inside Pyodide: the student's code, and the checks on it
lessons/       one folder per lesson — see lessons/README.md
```

**Real CPython runs the student's code; JavaScript runs the game.** That split
is deliberate. The lessons are full of error messages written in advance for
mistakes the student is about to make — `keys["Up"]` with a capital U, a `move`
with no `return` — and those only work if the thing running their code is
genuinely Python. Everything they type goes through Pyodide. The machinery
around it doesn't need to be Python, so it isn't.

The cost of that choice: each lesson's machinery exists twice, once in
`pochita/lessonN/lessonN.py` for the desktop and once in
`web/lessons/<id>/lesson.js` for here. Keep them in step. `lessons/README.md`
has the details that matter when porting one.

---

## Versions

Pinned in the files that load them:

| | | |
|---|---|---|
| Pyodide | `314.0.7` | `pyrunner.js` — ~6 MB on a first visit, cached after |
| Ace | `1.43.2` | `index.html` and `ACE_BASE` in `app.js` — the editor |
| marked | `16.4.1` | `index.html` — renders `lesson.md` into the steps |

If you bump Pyodide, check that `to_js` and `dict_converter` still behave the
way `pyrunner.py` expects.
