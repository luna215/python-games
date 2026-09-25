/* app.js — the shell around a lesson.
 *
 * The lesson text lives on the left. The right half shows one thing at a
 * time: the code they're writing, or the game it makes. Pressing "Run it"
 * swaps to the game; "Back to the code" swaps back.
 *
 * Knows nothing about any particular game — each lesson is a module under
 * lessons/<id>/lesson.js exporting the shape described in lessons/README.md.
 */

import { Stage, Input, Loop } from "./engine.js";
import { PyRunner } from "./pyrunner.js";

const LESSONS = [
  { id: "pochita-1", number: 1, title: "Pochita goes for a walk" },
  { id: "pochita-2", number: 2, title: "Bread and jam" },
];

const ACE_BASE =
  "https://cdn.jsdelivr.net/npm/ace-builds@1.43.2/src-min-noconflict";

const $ = (sel) => document.querySelector(sel);

const els = {
  pick: $("#pick"),
  progress: $("#progress"),
  lessonTitle: $("#lesson-title"),
  summary: $("#summary"),
  about: $("#about"),
  stepCount: $("#step-count"),
  stepBody: $("#step-body"),
  prev: $("#prev"),
  next: $("#next"),
  allSteps: $("#all-steps"),
  right: $("#right"),
  editor: $("#editor"),
  run: $("#run"),
  reset: $("#reset"),
  back: $("#back"),
  hint: $("#hint"),
  bootStatus: $("#boot-status"),
  message: $("#message"),
  canvas: $("#game"),
  gameView: $("#game-view"),
  codeView: $("#code-view"),
};

const MAC = navigator.platform.toLowerCase().includes("mac");
els.hint.textContent = MAC ? "⌘↵ to run it" : "Ctrl+↵ to run it";

let lesson = null;
let stage = null;
let input = null;
let loop = null;
let editor = null;
let starter = "";
let steps = [];
let at = 0;
let showingAll = false;
const py = new PyRunner();

const chosen = () => {
  const want = new URLSearchParams(location.search).get("lesson");
  return LESSONS.find((l) => l.id === want) || LESSONS[0];
};

const storeKey = (id) => `python-games:${id}`;
const stepKey = (id) => `python-games:step:${id}`;

/* localStorage throws in some privacy modes. Losing saved work is a nuisance;
 * a page that won't load at all is worse. */
const store = {
  get(key) {
    try { return localStorage.getItem(key); } catch (_) { return null; }
  },
  set(key, value) {
    try { localStorage.setItem(key, value); } catch (_) { /* nothing to do */ }
  },
};

/* ------------------------------------------------------------------ mode */

function setMode(mode) {
  els.right.dataset.mode = mode;

  if (mode === "game") {
    fitGame();                 // it had no size while it was hidden
    els.canvas.focus();
  } else {
    loop?.stop();
    editor?.resize();          // it had no size while it was hidden
    editor?.focus();
  }
}

const inGame = () => els.right.dataset.mode === "game";

/* --------------------------------------------------------- the lesson text */

/* lesson.md is one file split into a summary and then one chunk per step,
 * divided by `<!-- step -->` on its own line. An HTML comment, so the file
 * still reads as an ordinary document if you open it on GitHub. */
function parseLesson(markdown) {
  const chunks = markdown.split(/^<!--\s*step\s*-->\s*$/m);
  const head = chunks.shift() || "";

  const title = (head.match(/^#\s+(.+)$/m) || [, ""])[1].trim();
  const summary = head.replace(/^#\s+.+$/m, "").trim();

  const parsed = chunks
    .map((md) => md.trim())
    .filter(Boolean)
    .map((md) => ({
      title: (md.match(/^##\s+(.+)$/m) || [, "Step"])[1].trim(),
      html: marked.parse(md),
    }));

  return { title, summary: marked.parse(summary), steps: parsed };
}

function renderProgress() {
  els.progress.textContent = "";
  steps.forEach((_, i) => {
    const dot = document.createElement("i");
    if (i < at) dot.className = "done";
    if (i === at && !showingAll) dot.className = "here";
    els.progress.append(dot);
  });
}

function renderStep() {
  if (showingAll) {
    els.stepBody.className = "all";
    els.stepBody.textContent = "";
    steps.forEach((step, i) => {
      const section = document.createElement("section");
      section.innerHTML = step.html;
      const heading = section.querySelector("h2");
      if (heading) {
        heading.dataset.step = String(i);
        heading.title = "Go to this step";
      }
      els.stepBody.append(section);
    });
    els.stepCount.textContent = `All ${steps.length} steps`;
  } else {
    els.stepBody.className = "";
    els.stepBody.innerHTML = steps[at]?.html || "";
    els.stepCount.textContent = `Step ${at + 1} of ${steps.length}`;
  }

  els.stepBody.scrollTop = 0;
  markScrollable();
  els.prev.disabled = showingAll || at === 0;
  els.next.disabled = showingAll || at >= steps.length - 1;
  els.allSteps.setAttribute("aria-pressed", String(showingAll));
  renderProgress();
}

function goTo(index) {
  at = Math.max(0, Math.min(steps.length - 1, index));
  showingAll = false;
  els.about.open = at === 0;          // the summary matters on the way in
  store.set(stepKey(lesson.meta.id), String(at));
  renderStep();
}

/* Is there more step below the fold? Drives the fade at the bottom. */
function markScrollable() {
  const el = els.stepBody;
  el.classList.toggle(
    "more", el.scrollTop + el.clientHeight < el.scrollHeight - 2);
}

/* ------------------------------------------------------------- messages */

function clearMessage() {
  els.message.className = "";
  els.message.textContent = "";
  editor?.session.clearAnnotations();
}

function showMessage(kind, label, body, line = null) {
  els.message.className = `show ${kind}`;
  els.message.textContent = "";

  const tag = document.createElement("span");
  tag.className = "kind";
  tag.textContent = label;

  const text = document.createElement("div");
  text.textContent = body;          // never innerHTML — this quotes their code back

  els.message.append(tag, text);

  if (line && editor) {
    editor.session.setAnnotations([
      { row: Math.max(0, line - 1), column: 0, text: label, type: "error" },
    ]);
  }
}

function showError(err) {
  /* Most of the error messages in these programs were written for the exact
   * mistake being made, which is not true of programming in general. Worth
   * being able to tell those apart from the other kind at a glance. */
  if (err.expected) {
    showMessage("expected", "The lesson expected this", err.friendly, err.line);
  } else {
    showMessage("unexpected", "Python stopped", err.detail || err.message, err.line);
  }
}

function showPrinted(lines) {
  if (!lines.length) return;
  if (els.message.classList.contains("expected")) return;
  if (els.message.classList.contains("unexpected")) return;
  showMessage("output", "print()", lines.join("\n"));
}

/* ---------------------------------------------------------------- editor */

function setUpEditor(initial) {
  ace.config.set("basePath", ACE_BASE);
  editor = ace.edit(els.editor, {
    mode: "ace/mode/python",
    theme: "ace/theme/textmate",
    fontSize: "14px",
    tabSize: 4,
    useSoftTabs: true,
    showPrintMargin: false,
    highlightActiveLine: false,
    wrap: true,
  });
  editor.setValue(initial, -1);
  editor.session.on("change", () =>
    store.set(storeKey(lesson.meta.id), editor.getValue()));

  editor.commands.addCommand({
    name: "run",
    bindKey: { win: "Ctrl-Enter", mac: "Command-Enter" },
    exec: run,
  });
}

/* ------------------------------------------------------------------- run */

function run() {
  if (!py.ready || !lesson) return;
  loop.stop();
  clearMessage();
  py.clearPrinted();

  const meta = lesson.meta;
  try {
    py.load(editor.getValue());
    py.requireNames(meta.needs || []);
    py.validate(meta.checks || []);
    lesson.configure(py.constants(meta.consts || []));
    lesson.reset();
  } catch (err) {
    /* Couldn't even start — stay on the code, with the reason next to it. */
    showError(err);
    setMode("code");
    return;
  }

  els.canvas.classList.remove("paused");
  loop.now = 0;
  setMode("game");
  loop.start();
  showPrinted(py.printed);
}

function stopAndEdit() {
  loop?.stop();
  setMode("code");
}

function fitGame() {
  if (!stage) return;
  const box = els.gameView.getBoundingClientRect();
  if (box.width < 2 || box.height < 2) return;      // hidden
  stage.fit(box.width - 32, box.height - 32);
  redraw();
}

function redraw() {
  if (!lesson || !stage) return;
  try {
    lesson.draw(stage.ctx, loop ? loop.now : 0, input);
  } catch (_) {
    /* a failed run may have left nothing to draw yet */
  }
}

/* ------------------------------------------------------------------ boot */

async function main() {
  const entry = chosen();

  for (const l of LESSONS) {
    const opt = document.createElement("option");
    opt.value = l.id;
    opt.textContent = `Lesson ${l.number} — ${l.title}`;
    opt.selected = l.id === entry.id;
    els.pick.append(opt);
  }
  els.pick.addEventListener("change", () => {
    location.search = `?lesson=${els.pick.value}`;
  });

  const base = `./lessons/${entry.id}/`;
  const [mod, starterText, lessonText] = await Promise.all([
    import(`${base}lesson.js`),
    fetch(`${base}starter.py`).then((r) => r.text()),
    fetch(`${base}lesson.md`).then((r) => r.text()),
  ]);

  lesson = mod.default;
  starter = starterText.replace(/\s+$/, "") + "\n";

  const parsed = parseLesson(lessonText);
  steps = parsed.steps;
  at = Math.min(steps.length - 1,
                Math.max(0, parseInt(store.get(stepKey(entry.id)) || "0", 10)));

  document.title = `Lesson ${entry.number}: ${parsed.title} — Python Games`;
  els.lessonTitle.textContent = parsed.title;
  els.summary.innerHTML = parsed.summary;
  els.about.open = at === 0;
  renderStep();

  setUpEditor(store.get(storeKey(entry.id)) ?? starter);

  stage = new Stage(els.canvas, lesson.meta.width, lesson.meta.height);
  input = new Input(window, {
    ignore: (e) => Boolean(e.target.closest && e.target.closest("#editor")),
  });

  loop = new Loop({
    step(now) {
      try {
        lesson.step(now, input, py);
      } catch (err) {
        showError(err);
        els.canvas.classList.add("paused");
        setMode("code");                   // the reason belongs next to the code
        return false;
      }
    },
    draw(now) {
      lesson.draw(stage.ctx, now, input);
      showPrinted(py.printed);
    },
  });

  new ResizeObserver(() => { if (inGame()) fitGame(); }).observe(els.gameView);
  new ResizeObserver(() => { if (!inGame()) editor?.resize(); }).observe(els.codeView);
  els.stepBody.addEventListener("scroll", markScrollable);
  new ResizeObserver(markScrollable).observe(els.stepBody);

  els.canvas.addEventListener("mousemove", (e) => {
    input.pointerPos = stage.pointer(e);
    lesson.pointer?.("move", input.pointerPos);
  });
  els.canvas.addEventListener("mousedown", (e) => {
    els.canvas.focus();
    lesson.pointer?.("down", stage.pointer(e));
  });

  /* ESC quits the game in the desktop lessons. Same here — it puts the code
   * back up rather than closing a window. */
  window.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && inGame()) {
      e.preventDefault();
      stopAndEdit();
    }
  });

  els.prev.addEventListener("click", () => goTo(at - 1));
  els.next.addEventListener("click", () => goTo(at + 1));
  els.allSteps.addEventListener("click", () => {
    showingAll = !showingAll;
    renderStep();
  });
  els.stepBody.addEventListener("click", (e) => {
    const heading = e.target.closest("h2[data-step]");
    if (heading) goTo(Number(heading.dataset.step));
  });

  els.run.addEventListener("click", run);
  els.back.addEventListener("click", stopAndEdit);

  /* Reset throws away everything they've typed, so it asks twice — but with
   * the button itself rather than a browser dialog. */
  let resetArmed = null;
  els.reset.addEventListener("click", () => {
    if (!resetArmed) {
      els.reset.textContent = "Sure? This deletes your changes";
      resetArmed = setTimeout(() => {
        els.reset.textContent = "Reset";
        resetArmed = null;
      }, 4000);
      return;
    }
    clearTimeout(resetArmed);
    resetArmed = null;
    els.reset.textContent = "Reset";
    editor.setValue(starter, -1);
    store.set(storeKey(entry.id), starter);
    clearMessage();
  });

  py.onPrint = showPrinted;

  await lesson.preload();
  await py.boot((status) => (els.bootStatus.textContent = status));

  /* Python is ready, but nothing runs until they ask it to. */
  els.right.classList.add("ready");
  els.run.disabled = false;
  editor.focus();
}

main().catch((err) => {
  console.error(err);
  els.bootStatus.textContent = String(err.message || err);
});
