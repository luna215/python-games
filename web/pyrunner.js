/* pyrunner.js — boots Pyodide and talks to pyrunner.py.
 *
 * The game is JavaScript; everything in the editor pane is real CPython. All
 * the interesting logic lives next door in pyrunner.py — this file only
 * starts Python, hands it the student's source, and turns whatever comes back
 * out into something the editor pane can display.
 */

const PYODIDE_VERSION = "314.0.7";
const PYODIDE_URL = `https://cdn.jsdelivr.net/pyodide/v${PYODIDE_VERSION}/full/`;

/* Something the student can act on: either a message the lesson wrote for
 * this exact mistake, or a real traceback. `expected` says which, and the two
 * are shown differently — meeting a helpful error and meeting an unhelpful
 * one are different experiences and it is worth being able to tell. */
export class LessonError extends Error {
  constructor({ friendly, detail, line }) {
    super(friendly || detail || "Something went wrong.");
    this.name = "LessonError";
    this.friendly = friendly || null;
    this.detail = detail || null;
    this.line = typeof line === "number" ? line : null;
  }

  get expected() {
    return Boolean(this.friendly);
  }
}

function loadScript(src) {
  return new Promise((resolve, reject) => {
    const el = document.createElement("script");
    el.src = src;
    el.onload = resolve;
    el.onerror = () => reject(new Error("Couldn't download " + src));
    document.head.appendChild(el);
  });
}

export class PyRunner {
  constructor() {
    this.ready = false;
    this.printed = [];
    this.onPrint = null;
  }

  async boot(onStatus) {
    onStatus?.("Fetching Python…");
    const [glue] = await Promise.all([
      fetch(new URL("pyrunner.py", import.meta.url)).then((r) => {
        if (!r.ok) throw new Error("Couldn't fetch pyrunner.py");
        return r.text();
      }),
      loadScript(PYODIDE_URL + "pyodide.js"),
    ]);

    onStatus?.("Starting Python…");
    this.pyodide = await globalThis.loadPyodide({
      indexURL: PYODIDE_URL,
      stdout: (line) => this._print(line),
      stderr: (line) => this._print(line),
    });

    this.pyodide.runPython(glue);
    const g = this.pyodide.globals;
    this._py = {
      load: g.get("load"),
      need: g.get("need"),
      constants: g.get("constants"),
      validate: g.get("validate"),
      move1: g.get("move1"),
      move2: g.get("move2"),
      touching: g.get("touching"),
      lastError: g.get("last_error"),
    };
    this.ready = true;
  }

  /* print() is how you debug before you know what a debugger is, so it needs
   * somewhere to go other than the browser console. */
  _print(line) {
    this.printed.push(line);
    if (this.printed.length > 120) this.printed.shift();
    this.onPrint?.(this.printed);
  }

  clearPrinted() {
    this.printed = [];
    this.onPrint?.(this.printed);
  }

  /* Every call into Python goes through here, so whatever comes back out is a
   * LessonError that the editor pane knows how to show. */
  _guard(fn) {
    try {
      return fn();
    } catch (err) {
      let info = null;
      try {
        info = this._py.lastError();
      } catch (_) {
        /* the glue itself is broken — fall through to the raw message */
      }
      if (info && (info.friendly || info.detail)) throw new LessonError(info);
      throw new LessonError({
        detail: String(err && err.message ? err.message : err),
      });
    }
  }

  load(source) {
    return this._guard(() => this._py.load(source));
  }

  requireNames(names) {
    return this._guard(() => this._py.need(names));
  }

  validate(names) {
    return this._guard(() => this._py.validate(names));
  }

  /* Returns a plain JS object — BACKGROUND arrives as an array. */
  constants(names) {
    return this._guard(() => this._py.constants(names));
  }

  move1(x, speed) {
    return this._guard(() => this._py.move1(x, speed));
  }

  move2(x, y, held) {
    return this._guard(() =>
      this._py.move2(x, y, held.left, held.right, held.up, held.down));
  }

  touching(ax, ay, bx, by) {
    return this._guard(() => this._py.touching(ax, ay, bx, by));
  }
}
