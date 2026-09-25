/* engine.js — the bits every lesson needs to draw on a canvas.
 *
 * The desktop lessons get this from pygame. In the browser we do it by hand,
 * and the goal throughout is to match pygame's behaviour rather than to do
 * the browser-idiomatic thing — if a lesson says SPEED = 3 moves him three
 * pixels a frame, that has to stay true here, or the numbers in the lesson
 * cards stop meaning anything.
 */

/* ----------------------------------------------------------------- images */

export function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error("Couldn't load " + src));
    img.src = src;
  });
}

/* pygame.transform.scale() with no smoothing — nearest neighbour, which is
 * what keeps a 45-pixel-wide drawing crisp when you blow it up.
 *
 * pygame truncates fractional sizes, and so do we: that is the whole point of
 * `SIZE = 5.5` in lesson 1's "break it on purpose". 45 * 5.5 is 247.5, there
 * is no such thing as half a pixel, and the .5 is quietly thrown away. */
export function scaleImage(img, factor) {
  const w = Math.max(1, Math.trunc(img.width * factor));
  const h = Math.max(1, Math.trunc(img.height * factor));
  const off = document.createElement("canvas");
  off.width = w;
  off.height = h;
  const c = off.getContext("2d");
  c.imageSmoothingEnabled = false;
  c.drawImage(img, 0, 0, w, h);
  return off;
}

/* ------------------------------------------------------------------ paint */

export const rgb = (c) => `rgb(${c[0]},${c[1]},${c[2]})`;
export const rgba = (c, a) => `rgba(${c[0]},${c[1]},${c[2]},${a})`;

export function rect(ctx, colour, x, y, w, h, radius = 0, lineWidth = 0) {
  ctx.beginPath();
  if (radius > 0) ctx.roundRect(x, y, w, h, radius);
  else ctx.rect(x, y, w, h);
  paint(ctx, colour, lineWidth);
}

export function ellipse(ctx, colour, x, y, w, h, lineWidth = 0) {
  ctx.beginPath();
  ctx.ellipse(x + w / 2, y + h / 2, Math.abs(w / 2), Math.abs(h / 2), 0, 0, Math.PI * 2);
  paint(ctx, colour, lineWidth);
}

export function circle(ctx, colour, cx, cy, r) {
  ctx.beginPath();
  ctx.arc(cx, cy, Math.max(0, r), 0, Math.PI * 2);
  paint(ctx, colour, 0);
}

export function polygon(ctx, colour, points, lineWidth = 0) {
  ctx.beginPath();
  points.forEach(([x, y], i) => (i ? ctx.lineTo(x, y) : ctx.moveTo(x, y)));
  ctx.closePath();
  paint(ctx, colour, lineWidth);
}

export function line(ctx, colour, x1, y1, x2, y2, width = 1) {
  ctx.beginPath();
  ctx.moveTo(x1, y1);
  ctx.lineTo(x2, y2);
  ctx.strokeStyle = rgb(colour);
  ctx.lineWidth = width;
  ctx.stroke();
}

function paint(ctx, colour, lineWidth) {
  if (lineWidth > 0) {
    ctx.strokeStyle = rgb(colour);
    ctx.lineWidth = lineWidth;
    ctx.stroke();
  } else {
    ctx.fillStyle = rgb(colour);
    ctx.fill();
  }
}

/* pygame.font.Font(None, n) is freesansbold at point size n. Measured against
 * the real thing: ptsize 26 renders 17px tall, 34 renders 23px, so 0.68 is the
 * conversion to a CSS pixel size. Near enough for a HUD. */
export function font(ptsize) {
  return `bold ${Math.round(ptsize * 0.68)}px Arial, Helvetica, sans-serif`;
}

export function text(ctx, str, ptsize, colour, x, y) {
  ctx.font = font(ptsize);
  ctx.textBaseline = "top";
  ctx.textAlign = "left";
  ctx.fillStyle = rgb(colour);
  ctx.fillText(str, x, y);
}

export function textWidth(ctx, str, ptsize) {
  ctx.font = font(ptsize);
  return ctx.measureText(str).width;
}

/* The wrap() helper from lesson2.py, same logic. */
export function wrapText(ctx, str, ptsize, maxWidth) {
  const lines = [];
  let cur = "";
  for (const word of str.split(/\s+/).filter(Boolean)) {
    const trial = cur ? cur + " " + word : word;
    if (!cur || textWidth(ctx, trial, ptsize) <= maxWidth) cur = trial;
    else {
      lines.push(cur);
      cur = word;
    }
  }
  if (cur) lines.push(cur);
  return lines;
}

/* ------------------------------------------------------------------ stage */

/* Sizes the canvas to fill its pane while keeping the lesson's aspect ratio,
 * and hands drawing code plain logical coordinates — so a lesson can say
 * "900 wide" and mean it, whatever the window is doing. */
export class Stage {
  constructor(canvas, width, height) {
    this.canvas = canvas;
    this.width = width;
    this.height = height;
    this.ctx = canvas.getContext("2d");
    this.scale = 1;
  }

  fit(paneWidth, paneHeight) {
    const dpr = window.devicePixelRatio || 1;
    const scale = Math.min(paneWidth / this.width, paneHeight / this.height);
    if (!(scale > 0)) return;
    this.scale = scale;
    this.canvas.style.width = `${this.width * scale}px`;
    this.canvas.style.height = `${this.height * scale}px`;
    this.canvas.width = Math.round(this.width * scale * dpr);
    this.canvas.height = Math.round(this.height * scale * dpr);
    this.ctx.setTransform(scale * dpr, 0, 0, scale * dpr, 0, 0);
    this.ctx.imageSmoothingEnabled = false;
  }

  /* Where a mouse event landed, in logical coordinates. */
  pointer(event) {
    const box = this.canvas.getBoundingClientRect();
    return {
      x: (event.clientX - box.left) / this.scale,
      y: (event.clientY - box.top) / this.scale,
    };
  }
}

/* ------------------------------------------------------------------ input */

const KEY_NAMES = {
  ArrowLeft: "left", ArrowRight: "right", ArrowUp: "up", ArrowDown: "down",
  a: "left", d: "right", w: "up", s: "down",
  A: "left", D: "right", W: "up", S: "down",
};

export class Input {
  /* `ignore` gets the event and says whether it belongs to something else.
   * The editor needs its arrow keys for moving the cursor around, so the game
   * has to keep its hands off anything typed in there. */
  constructor(target, { ignore = () => false } = {}) {
    this.held = { left: false, right: false, up: false, down: false };
    this.pointerPos = { x: -1, y: -1 };
    this._pressed = new Set();

    this._down = (e) => {
      if (ignore(e)) return;
      const name = KEY_NAMES[e.key];
      if (name) {
        this.held[name] = true;
        e.preventDefault();          // stop the arrow keys scrolling the page
      }
      this._pressed.add(e.key);
    };
    this._up = (e) => {
      if (ignore(e)) return;
      const name = KEY_NAMES[e.key];
      if (name) this.held[name] = false;
      this._pressed.delete(e.key);
    };
    this._blur = () => {
      for (const k of Object.keys(this.held)) this.held[k] = false;
      this._pressed.clear();
    };

    target.addEventListener("keydown", this._down);
    target.addEventListener("keyup", this._up);
    window.addEventListener("blur", this._blur);
  }

  /* True once, then forgotten — for things like ENTER on the win screen. */
  takePress(...keys) {
    for (const k of keys) {
      if (this._pressed.has(k)) {
        this._pressed.delete(k);
        return true;
      }
    }
    return false;
  }
}

/* ------------------------------------------------------------------- loop */

export const FPS = 60;
const STEP_MS = 1000 / FPS;

/* A fixed 60Hz timestep, deliberately.
 *
 * pygame's clock.tick(60) means SPEED is "pixels per frame at 60 frames a
 * second". requestAnimationFrame runs at whatever the display does, which on a
 * ProMotion Mac is 120Hz — and everything would move at double speed, making
 * every number in the lesson cards wrong. So we advance the game in exact 60Hz
 * steps and draw whenever the browser asks, however often that is. */
export class Loop {
  constructor({ step, draw }) {
    this.step = step;
    this.draw = draw;
    this.now = 0;                 // mirrors pygame.time.get_ticks()
    this.running = false;
    this._acc = 0;
    this._last = 0;
    this._raf = null;
  }

  start() {
    if (this.running) return;
    this.running = true;
    this._last = performance.now();
    this._raf = requestAnimationFrame(this._tick);
  }

  stop() {
    this.running = false;
    if (this._raf !== null) cancelAnimationFrame(this._raf);
    this._raf = null;
  }

  _tick = (stamp) => {
    if (!this.running) return;
    this._acc += stamp - this._last;
    this._last = stamp;

    // A backgrounded tab hands back a huge gap. Don't try to catch up on it.
    if (this._acc > STEP_MS * 5) this._acc = STEP_MS * 5;

    while (this._acc >= STEP_MS) {
      this.now += STEP_MS;
      this._acc -= STEP_MS;
      if (this.step(this.now) === false) {   // the step asked us to stop
        this.stop();
        return;
      }
    }
    this.draw(this.now);
    this._raf = requestAnimationFrame(this._tick);
  };
}
