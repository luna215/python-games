"""The Python side of the browser tutorials.

This runs inside Pyodide, once, when the page loads. It never touches the
game — all it does is run the student's code block, check it over, and hand
the answers back to the JavaScript that draws things.

Everything the student writes is genuinely Python, which is the whole reason
this file exists. The lessons are full of error messages written in advance
for mistakes the student is about to make, and those only work if the thing
running their code is really Python.

The messages below are lifted from lesson1.py and lesson2.py on purpose. If
you change the wording in one place, change it in the other.
"""

import traceback

import js
from pyodide.ffi import to_js

FILENAME = "your code"          # what the student's code is called in a traceback


class Friendly(Exception):
    """A message written in advance for a mistake the lesson expects.

    Everything else that goes wrong is a real traceback. The two are shown
    differently, because knowing which kind you are looking at is worth
    something on its own.
    """

    def __init__(self, message, line=None):
        super().__init__(message)
        self.message = message
        self.line = line


class Keys(dict):
    """A dict that explains itself when you ask it something odd.

    Straight out of lesson2.py, so the browser and the terminal say the same
    things word for word.
    """

    def __missing__(self, name):
        raise Friendly(
            "There's no key called %r.\n"
            "The four you can ask about are: left, right, up, down.\n"
            "They're all lowercase — check your spelling." % (name,))

    def __getattr__(self, name):
        if name.startswith("__"):            # Python's own private questions
            raise AttributeError(name)
        raise Friendly(
            "You wrote  keys.%s  — it needs square brackets and quotes:\n"
            '\n    keys["%s"]' % (name, name))


_ns = {}
_keys = Keys(left=False, right=False, up=False, down=False)
_last = {"friendly": None, "line": None, "detail": None}


# --------------------------------------------------------- reporting it back

def _student_line(exc):
    """The deepest line number inside the student's own code, if any."""
    line = None
    tb = exc.__traceback__
    while tb is not None:
        if tb.tb_frame.f_code.co_filename == FILENAME:
            line = tb.tb_lineno
        tb = tb.tb_next
    return line


def _detail(exc):
    """A traceback with our own plumbing filtered out of it."""
    parts = traceback.format_exception(type(exc), exc, exc.__traceback__)
    keep = []
    for part in parts:
        if part.startswith("Traceback"):
            continue
        if part.lstrip().startswith("File ") and FILENAME not in part:
            continue
        keep.append(part)
    return "".join(keep).strip() or str(exc)


def _record(exc):
    if isinstance(exc, Friendly):
        _last["friendly"] = exc.message
        _last["line"] = exc.line
        _last["detail"] = None
    else:
        _last["friendly"] = None
        _last["line"] = _student_line(exc)
        _last["detail"] = _detail(exc)


def reported(fn):
    """Remember why something blew up, so JavaScript can show it properly."""
    def wrapper(*args):
        try:
            return fn(*args)
        except BaseException as exc:
            _record(exc)
            raise
    return wrapper


def last_error():
    return to_js(_last, dict_converter=js.Object.fromEntries)


# ------------------------------------------------------------- running it

@reported
def load(source):
    """Run the student's whole code block, fresh, into its own namespace.

    All of it together, every time — so that editing SPEED and pressing Run
    means move() sees the new SPEED. Their functions read the constants as
    module globals, exactly as they do on the desktop.

    It goes into its own dict rather than into these globals, so nothing they
    write can stand on the machinery by accident.
    """
    global _ns
    try:
        code = compile(source, FILENAME, "exec")
    except SyntaxError as exc:
        raise Friendly(
            "Python couldn't read your code. The problem is on or just "
            "before line %s:\n\n    %s\n\n%s"
            % (exc.lineno, (exc.text or "").strip(), exc.msg), exc.lineno)
    ns = {}
    exec(code, ns)
    _ns = ns
    return True


@reported
def need(names):
    for name in names:
        if name not in _ns:
            raise Friendly(
                "Your code doesn't have anything called %s in it.\n"
                "The game looks for it every time it runs, so it has to be "
                "there." % (name,))
    return True


@reported
def constants(names):
    out = {}
    for name in names:
        if name not in _ns:
            raise Friendly(
                "Your code doesn't have anything called %s in it.\n"
                "The game reads it every time it runs, so it has to be "
                "there." % (name,))
        out[name] = _ns[name]
    return to_js(out, dict_converter=js.Object.fromEntries)


# ------------------------------------------------ the machinery's own checks

_CHECKS = {}


def _check(name):
    def register(fn):
        _CHECKS[name] = fn
        return fn
    return register


@_check("SIZE")
def _check_size(value):
    if not isinstance(value, int) or value < 1:
        raise Friendly(
            "SIZE is %r. It has to be a whole number, 1 or more.\n"
            "It's how many times bigger than the original drawing to make "
            "him." % (value,))


@_check("BACKGROUND")
def _check_background(value):
    if (not isinstance(value, (tuple, list)) or len(value) != 3
            or not all(isinstance(c, int) and 0 <= c <= 255 for c in value)):
        raise Friendly(
            "BACKGROUND is %r.\n"
            "It needs three whole numbers between 0 and 255, like "
            "(246, 234, 220)\n— one each for red, green and blue." % (value,))


@_check("REACH")
def _check_reach(value):
    if not isinstance(value, (int, float)) or not 1 <= value <= 200:
        raise Friendly(
            "REACH is %r. It has to be between 1 and 200.\n"
            "Any bigger and he'd be touching a thing the moment it appeared,\n"
            "which would hand you the whole game without you moving."
            % (value,))


@_check("NEEDED")
def _check_needed(value):
    if not isinstance(value, int) or value < 1:
        raise Friendly(
            "NEEDED is %r. It has to be a whole number, 1 or more.\n"
            "It's how many of each thing Pochita has to fetch before Denji\n"
            "comes out — and at 0 he'd come out before you'd done anything."
            % (value,))


@reported
def validate(names):
    """Only the checks this lesson asks for.

    Lesson 1 deliberately does NOT check SIZE. `SIZE = 5.5` is one of its
    break-it-on-purpose exercises and the entire point is that nothing warns
    you — he just goes quietly lopsided. Lesson 2 does check it. Keep the
    difference.
    """
    for name in names:
        if name in _CHECKS and name in _ns:
            _CHECKS[name](_ns[name])
    return True


# -------------------------------------------------------- called every frame

def _their(name, what):
    fn = _ns.get(name)
    if fn is None:
        raise Friendly(
            "There's no function called %s in your code.\n%s" % (name, what))
    if not callable(fn):
        raise Friendly(
            "%s is in your code, but it isn't a function — it's %r.\n"
            "It needs to start with  def %s(" % (name, fn, name))
    return fn


def _two_numbers(result, call, ret):
    if result is None:
        raise Friendly(
            "%s didn't hand anything back.\n"
            "It needs `%s` as its last line." % (call, ret))
    try:
        first, second = result
    except (TypeError, ValueError):
        raise Friendly(
            "%s has to hand back exactly two numbers, like `%s`.\n"
            "Right now it hands back: %r" % (call, ret, result))
    try:
        pair = [float(first), float(second)]
    except (TypeError, ValueError):
        raise Friendly(
            "%s has to hand back two numbers, like `%s`.\n"
            "Right now it hands back: %r" % (call, ret, result))
    return to_js(pair)


@reported
def move1(x, speed):
    """Lesson 1 — the student's move(x, speed), once per frame."""
    move = _their(
        "move",
        "The game calls it sixty times a second, so it has to be there.")
    try:
        result = move(x, speed)
    except Friendly:
        raise
    except NameError as problem:
        raise Friendly(
            "move() uses a name Python doesn't know: %s\n"
            "\nNames have to match exactly: SPEED is not the same as speed."
            % (problem,))
    return _two_numbers(result, "move()", "return x, speed")


@reported
def move2(x, y, left, right, up, down):
    """Lesson 2 — the student's move(x, y, keys), once per frame."""
    move = _their(
        "move",
        "The game calls it sixty times a second, so it has to be there.")
    _keys["left"] = bool(left)
    _keys["right"] = bool(right)
    _keys["up"] = bool(up)
    _keys["down"] = bool(down)
    try:
        result = move(x, y, _keys)
    except Friendly:
        raise
    except NameError as problem:
        raise Friendly(
            "move() uses a name Python doesn't know: %s\n"
            "\nIf you meant one of the arrow keys, it needs BOTH quotes and\n"
            "square brackets:\n"
            '\n    keys["up"]        not   keys[up]\n'
            "\nAnd names have to match exactly: SPEED is not the same as "
            "speed." % (problem,))
    return _two_numbers(result, "move()", "return x, y")


@reported
def touching(ax, ay, bx, by):
    """Lesson 2 — the student's is_touching(), twice per frame."""
    fn = _their(
        "is_touching",
        "The game uses it to decide whether he's reached something.")
    try:
        result = fn(ax, ay, bx, by)
    except Friendly:
        raise
    except NameError as problem:
        raise Friendly(
            "is_touching() uses a name Python doesn't know: %s\n"
            "\nNames have to match exactly, and the four it is handed are\n"
            "called ax, ay, bx and by." % (problem,))
    if result is None:
        raise Friendly(
            "is_touching() didn't hand anything back.\n"
            "It needs to end with a `return`, and hand back True or False.")
    return bool(result)
