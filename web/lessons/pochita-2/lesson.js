/* Lesson 2 — Bread and jam.
 *
 * THE MACHINERY, in JavaScript. This is the same program as
 * pochita/lesson2/lesson2.py from `import pygame` downwards: same sizes, same
 * colours, same order of operations, same placement rules. If you change one,
 * change the other.
 *
 * Two behaviours here are what the lesson is built on, and both have to
 * survive any edit to this file:
 *   - the jam is unreachable until they write vertical movement
 *   - SPEED = 150 makes him tunnel past the bread and stall forever
 */

import {
  loadImage, scaleImage, rect, ellipse, circle, polygon,
  text, textWidth, wrapText, rgb, rgba,
} from "../../engine.js";

const WIDTH = 900;
const HEIGHT = 600;

const BREAD_W = 46, BREAD_H = 36;     // wide: you run at it sideways
const JAM_W = 32, JAM_H = 46;         // tall: you have to go up or down for it
const MARGIN = 60;

const GRID = [236, 223, 208];
const HUD_INK = [120, 100, 88];
const HUD_FAINT = [168, 150, 136];

const DENJI_HAIR = [236, 201, 96];
const DENJI_HAIR_DARK = [196, 158, 58];
const DENJI_SKIN = [250, 214, 180];
const DENJI_LINE = [54, 42, 38];
const DENJI_SHIRT = [246, 246, 242];
const DENJI_TIE = [58, 52, 64];
const BREAD_CRUMB = [196, 142, 74];
const JAM_CRUMB = [196, 52, 70];

const CRUMB_SECONDS = 0.7;

const SPRITES = new URL("../../../pochita/sprites/", import.meta.url);

const raw = { left: [], right: [] };
const walk = { left: [], right: [] };

let C = {};
let pochitaW = 0, pochitaH = 0;

let x = 0, y = 0;
let breadGot = 0, jamGot = 0;
let breadX = 0, breadY = 0, jamX = 0, jamY = 0;
let won = false;
let facing = "right";
let frame = 0;
let lastFrameChange = 0;
let crumbs = [];
let mouse = { x: -1, y: -1 };
let denjiBig = [];

/* ------------------------------------------------------------ where things go */

/* Bread lands further along the same row he's standing on. It has to land
 * outside REACH, or he'd pick the new one up the instant it appeared and keep
 * doing that forever. If nothing far enough turns up, use the furthest we saw. */
function newBread(px, py) {
  const far = Math.max(260, C.REACH + 40);
  let best = MARGIN, bestGap = -1;
  for (let i = 0; i < 120; i++) {
    const bx = MARGIN + Math.floor(Math.random() * (WIDTH - 2 * MARGIN + 1));
    const gap = Math.abs(bx - px);
    if (gap > bestGap) { best = bx; bestGap = gap; }
    if (gap > far) return [bx, py];
  }
  return [best, py];
}

/* Jam lands further up or down the same column he's standing in. */
function newJam(px, py) {
  const far = Math.max(170, C.REACH + 40);
  let best = MARGIN, bestGap = -1;
  for (let i = 0; i < 120; i++) {
    const jy = MARGIN + Math.floor(Math.random() * (HEIGHT - 2 * MARGIN + 1));
    const gap = Math.abs(jy - py);
    if (gap > bestGap) { best = jy; bestGap = gap; }
    if (gap > far) return [px, jy];
  }
  return [px, best];
}

/* ---------------------------------------------------------------- the food */

/* pygame's Rect.inflate(-n, -n) shrinks by n overall, keeping the centre. */
function centred(cx, cy, w, h) {
  return [cx - w / 2, cy - h / 2, w, h];
}

function drawBread(ctx, cx, cy, scale = 1.0) {
  const w = BREAD_W * scale, h = BREAD_H * scale;
  rect(ctx, [196, 142, 74], ...centred(cx, cy, w, h), 9 * scale);
  rect(ctx, [238, 206, 150],
    ...centred(cx, cy, w - 10 * scale, h - 10 * scale), 6 * scale);
}

function drawJam(ctx, cx, cy, scale = 1.0) {
  const w = JAM_W * scale, h = JAM_H * scale;
  const bodyH = h - 12 * scale;
  rect(ctx, [162, 38, 54], ...centred(cx, cy + 6 * scale, w, bodyH), 7 * scale);
  rect(ctx, [218, 72, 90],
    ...centred(cx, cy + 6 * scale, w - 10 * scale, bodyH - 12 * scale), 5 * scale);
  rect(ctx, [126, 98, 64],
    ...centred(cx, cy - h / 2 + 7 * scale, w + 6 * scale, 13 * scale), 4 * scale);
}

/* ------------------------------------------------------------------ Denji */

/* Drawn small and blown up, so he comes out chunky like the sprites do. */
function denjiSurface(chomp) {
  const w = 36, h = 56, cx = 18;
  const off = document.createElement("canvas");
  off.width = w;
  off.height = h;
  const c = off.getContext("2d");

  const body = [cx - 11, 34, 22, 20];
  rect(c, DENJI_SHIRT, ...body, 4);
  rect(c, DENJI_LINE, ...body, 4, 1);
  polygon(c, DENJI_TIE,
    [[cx, 35], [cx - 3, 41], [cx, 52], [cx + 3, 41]]);

  const head = [cx - 12, 12, 24, 25];
  ellipse(c, DENJI_SKIN, ...head);
  ellipse(c, DENJI_LINE, ...head, 1);

  const mouth = [cx - 5, 27, 10, 2 + Math.trunc(7 * chomp)];
  ellipse(c, [122, 44, 48], ...mouth);
  ellipse(c, DENJI_LINE, ...mouth, 1);

  ellipse(c, DENJI_LINE, cx - 7, 23, 3, 4);
  ellipse(c, DENJI_LINE, cx + 4, 23, 3, 4);

  // hair: the cap first, then spikes on top of it so they actually show
  const cap = [cx - 13, 9, 26, 13];
  ellipse(c, DENJI_HAIR, ...cap);
  for (const [dx, tall] of [[-11, 7], [-6, 11], [0, 12], [6, 11], [11, 7]]) {
    polygon(c, DENJI_HAIR,
      [[cx + dx - 5, 14], [cx + dx, 14 - tall], [cx + dx + 5, 14]]);
  }
  ellipse(c, DENJI_HAIR_DARK, ...cap, 1);

  // built big, because he's the reward and should fill some space
  const big = document.createElement("canvas");
  big.width = 108;
  big.height = 168;
  const b = big.getContext("2d");
  b.imageSmoothingEnabled = false;
  b.drawImage(off, 0, 0, 108, 168);
  return big;
}

/* ----------------------------------------------------------------- crumbs */

function spawnCrumbs(cx, cy, kind, when) {
  const bits = [];
  for (let i = 0; i < 8; i++) {
    bits.push([Math.random() * 2 - 1, -0.3 - Math.random() * 1.2]);
  }
  crumbs.push({ x: cx, y: cy, kind, born: when, bits });
}

function drawCrumbs(ctx, when) {
  for (const c of crumbs.slice()) {
    const age = (when - c.born) / 1000;
    if (age >= CRUMB_SECONDS) {
      crumbs.splice(crumbs.indexOf(c), 1);
      continue;
    }
    const along = age / CRUMB_SECONDS;
    const colour = c.kind === "bread" ? BREAD_CRUMB : JAM_CRUMB;
    for (const [vx, vy] of c.bits) {
      const px = c.x + vx * 86 * along;
      const py = c.y - 44 + vy * 86 * along + 150 * along * along;
      circle(ctx, colour, Math.trunc(px), Math.trunc(py),
        Math.max(1, Math.trunc(5 * (1 - along))));
    }
  }
}

/* ------------------------------------------------------------- win screen */

/* A long WIN_MESSAGE pushes the picture and the button down. Past a point
 * there's no room left, so the message gets trimmed rather than shoving Denji
 * off the bottom — he's the whole reward. */
function winLayout(ctx) {
  let lines = wrapText(ctx, C.WIN_MESSAGE, 38, WIDTH - 150);
  const tall = 168;
  const textTop = 84;
  let denjiTop = textTop + lines.length * 42 + 26;

  const button = { w: 230, h: 60, x: (WIDTH - 230) / 2, y: denjiTop + tall + 28 };

  if (button.y + button.h > HEIGHT - 16) {
    button.y = HEIGHT - 16 - button.h;
    denjiTop = button.y - 28 - tall;
    const room = Math.max(1, Math.floor((denjiTop - 26 - textTop) / 42));
    lines = lines.slice(0, room);
  }
  return { lines, textTop, denjiTop, button };
}

function inButton(b, p) {
  return p.x >= b.x && p.x <= b.x + b.w && p.y >= b.y && p.y <= b.y + b.h;
}

function drawWinScreen(ctx, when) {
  ctx.fillStyle = rgba([26, 18, 13], 238 / 255);
  ctx.fillRect(0, 0, WIDTH, HEIGHT);

  const { lines, textTop, denjiTop, button } = winLayout(ctx);

  lines.forEach((line, i) => {
    const w = textWidth(ctx, line, 38);
    text(ctx, line, 38, [252, 246, 238], (WIDTH - w) / 2, textTop + i * 42);
  });

  const chomp = Math.abs(Math.sin(when / 1000 * 9.0));
  const denji = denjiBig[Math.min(5, Math.trunc(chomp * 5.99))];
  ctx.drawImage(denji, (WIDTH - denji.width) / 2, denjiTop);

  // a slice of bread on one side of him and the jam on the other
  const bob = Math.sin(when / 1000 * 3.0) * 5;
  const foodY = denjiTop + denji.height / 2;
  drawBread(ctx, WIDTH / 2 - 132, Math.trunc(foodY + bob), 1.5);
  drawJam(ctx, WIDTH / 2 + 132, Math.trunc(foodY - bob), 1.5);

  const hot = inButton(button, mouse);
  rect(ctx, hot ? [250, 226, 168] : [232, 200, 132],
    button.x, button.y, button.w, button.h, 12);
  rect(ctx, [120, 92, 48], button.x, button.y, button.w, button.h, 12, 2);

  const label = "Play again";
  const lw = textWidth(ctx, label, 32);
  text(ctx, label, 32, [58, 44, 32],
    button.x + (button.w - lw) / 2, button.y + button.h / 2 - 11);
}

/* ------------------------------------------------------------------ round */

function startRound() {
  x = WIDTH / 2;
  y = HEIGHT / 2;
  breadGot = 0;
  jamGot = 0;
  [breadX, breadY] = newBread(x, y);
  [jamX, jamY] = newJam(x, y);
  won = false;
  crumbs = [];
  facing = "right";
  frame = 0;
  lastFrameChange = 0;
}

export default {
  meta: {
    id: "pochita-2",
    width: WIDTH,
    height: HEIGHT,
    consts: ["SPEED", "SIZE", "REACH", "NEEDED", "BACKGROUND", "WIN_MESSAGE"],
    checks: ["SIZE", "BACKGROUND", "REACH", "NEEDED"],
    needs: ["move", "is_touching"],
    note: "numbers, and two functions",
  },

  async preload() {
    for (const side of ["left", "right"]) {
      raw[side] = await Promise.all(
        [1, 2, 3, 4].map((n) =>
          loadImage(new URL(`pochita_${side}_${n}.png`, SPRITES).href)));
    }
    denjiBig = [0, 1, 2, 3, 4, 5].map((i) => denjiSurface(i / 5.0));
  },

  configure(consts) {
    C = consts;
    for (const side of ["left", "right"]) {
      walk[side] = raw[side].map((img) => scaleImage(img, C.SIZE));
    }
    pochitaW = walk.left[0].width;
    pochitaH = walk.left[0].height;
  },

  reset() {
    startRound();
  },

  pointer(kind, pos) {
    mouse = pos;
    if (kind === "down" && won) {
      /* winLayout needs a ctx only to measure text; the live one is fine. */
      const ctx = document.querySelector("#game").getContext("2d");
      if (inButton(winLayout(ctx).button, pos)) startRound();
    }
  },

  step(now, input, py) {
    if (won) {
      if (input.takePress("Enter", " ")) startRound();
      return;
    }

    const wasX = x, wasY = y;
    [x, y] = py.move2(x, y, input.held);

    // keep him on the floor you can see
    x = Math.max(pochitaW / 2, Math.min(WIDTH - pochitaW / 2, x));
    y = Math.max(pochitaH / 2, Math.min(HEIGHT - pochitaH / 2, y));

    const moved = Math.abs(x - wasX) > 0.01 || Math.abs(y - wasY) > 0.01;
    if (x < wasX) facing = "left";
    else if (x > wasX) facing = "right";

    // his legs only move while he does
    if (moved && now - lastFrameChange >= 120) {
      frame = (frame + 1) % 4;
      lastFrameChange = now;
    }
    if (!moved) frame = 0;

    if (py.touching(x, y, breadX, breadY)) {
      breadGot += 1;
      spawnCrumbs(breadX, breadY, "bread", now);
      [breadX, breadY] = newBread(x, y);
    }
    if (py.touching(x, y, jamX, jamY)) {
      jamGot += 1;
      spawnCrumbs(jamX, jamY, "jam", now);
      [jamX, jamY] = newJam(x, y);
    }

    if (breadGot >= C.NEEDED && jamGot >= C.NEEDED) won = true;
  },

  draw(ctx, now, input) {
    if (!walk.left.length) return;

    rect(ctx, C.BACKGROUND, 0, 0, WIDTH, HEIGHT);
    for (let gx = 0; gx < WIDTH; gx += 60) {
      ctx.beginPath();
      ctx.moveTo(gx + 0.5, 0);
      ctx.lineTo(gx + 0.5, HEIGHT);
      ctx.strokeStyle = rgb(GRID);
      ctx.lineWidth = 1;
      ctx.stroke();
    }
    for (let gy = 0; gy < HEIGHT; gy += 60) {
      ctx.beginPath();
      ctx.moveTo(0, gy + 0.5);
      ctx.lineTo(WIDTH, gy + 0.5);
      ctx.strokeStyle = rgb(GRID);
      ctx.lineWidth = 1;
      ctx.stroke();
    }

    drawBread(ctx, breadX, breadY);
    drawJam(ctx, jamX, jamY);
    ctx.drawImage(walk[facing][frame],
      Math.trunc(x - pochitaW / 2), Math.trunc(y - pochitaH / 2));
    drawCrumbs(ctx, now);

    if (won) {
      drawWinScreen(ctx, now);
      return;
    }

    text(ctx,
      `bread ${breadGot} / ${C.NEEDED}     jam ${jamGot} / ${C.NEEDED}`,
      34, HUD_INK, 16, 14);
    text(ctx, `x = ${Math.trunc(x)}    y = ${Math.trunc(y)}`,
      26, HUD_FAINT, 16, 50);

    const held = ["left", "right", "up", "down"]
      .filter((n) => input.held[n]).join(" ");
    text(ctx, `holding: ${held || "nothing"}`, 26, HUD_FAINT, 16, 74);
  },
};
