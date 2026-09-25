/* Lesson 1 — Pochita goes for a walk.
 *
 * THE MACHINERY, in JavaScript. This is the same program as
 * pochita/lesson1/lesson1.py from `import pygame` downwards: same window size,
 * same colours, same order of operations. If you change one, change the other.
 */

import { loadImage, scaleImage, rect, line, text } from "../../engine.js";

const WIDTH = 900;
const HEIGHT = 500;
const GROUND = 60;              // how much floor to draw under him

const GROUND_FILL = [206, 188, 170];
const GROUND_LINE = [150, 130, 116];
const HUD_INK = [120, 100, 88];

/* Every lesson shares the same artwork, three folders up. */
const SPRITES = new URL("../../../pochita/sprites/", import.meta.url);

const raw = { left: [], right: [] };      // the drawings as they come off disk
const walk = { left: [], right: [] };     // ...and blown up by SIZE

let C = {};                     // whatever the student's code currently says
let x = 100;
let speed = 0;
let frame = 0;
let lastFrameChange = 0;
let pochitaW = 0;

export default {
  meta: {
    id: "pochita-1",
    width: WIDTH,
    height: HEIGHT,
    consts: ["SPEED", "POCHITA_Y", "SIZE", "FRAME_MS", "BACKGROUND"],

    /* Deliberately no SIZE check here. `SIZE = 5.5` is break-it-on-purpose
     * number 4 and the whole point is that nothing warns you. */
    checks: ["BACKGROUND"],

    needs: ["move"],
    note: "numbers, a colour, and one function",
  },

  async preload() {
    for (const side of ["left", "right"]) {
      raw[side] = await Promise.all(
        [1, 2, 3, 4].map((n) =>
          loadImage(new URL(`pochita_${side}_${n}.png`, SPRITES).href)));
    }
  },

  configure(consts) {
    C = consts;
    for (const side of ["left", "right"]) {
      walk[side] = raw[side].map((img) => scaleImage(img, C.SIZE));
    }
    pochitaW = walk.left[0].width;
  },

  reset() {
    x = 100;
    speed = C.SPEED;
    frame = 0;
    lastFrameChange = 0;
  },

  step(now, input, py) {
    [x, speed] = py.move1(x, speed);

    // if nobody turned him around, wrap him to the other side
    if (x > WIDTH) x = -pochitaW;
    else if (x < -pochitaW) x = WIDTH;

    // hold each drawing of his legs for FRAME_MS before moving to the next
    if (now - lastFrameChange >= Math.max(16, C.FRAME_MS)) {
      frame = (frame + 1) % 4;
      lastFrameChange = now;
    }
  },

  draw(ctx) {
    if (!walk.left.length) return;          // nothing has run successfully yet

    const facing = speed > 0 ? "right" : "left";

    rect(ctx, C.BACKGROUND, 0, 0, WIDTH, HEIGHT);
    rect(ctx, GROUND_FILL, 0, HEIGHT - GROUND, WIDTH, GROUND);
    line(ctx, GROUND_LINE, 0, HEIGHT - GROUND, WIDTH, HEIGHT - GROUND, 3);

    ctx.drawImage(walk[facing][frame], Math.trunc(x), C.POCHITA_Y);

    text(ctx,
      `x = ${Math.trunc(x)}     speed = ${Math.trunc(speed)}     facing ${facing}`,
      26, HUD_INK, 16, 14);
  },
};
