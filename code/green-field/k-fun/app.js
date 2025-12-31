/*
  Kaleidoscope App (vanilla JS, ES6+)
  Architecture:
  - Defaults (config + bounds)
  - Utilities
  - KaleidoscopeRenderer (drawing + symmetry logic)
  - InputController (pointer + keyboard)
  - UIController (DOM controls)
  - App (init, resize, loop)
*/

// ----- Defaults / Config -----
const Defaults = Object.freeze({
  segments: 12,
  minSegments: 6,
  maxSegments: 24,
  paused: false,
  baseRotationSpeed: 0.5, // radians per second baseline
  pointerRotationFactor: 2.2, // scales pointer dx influence
  pointerOffsetFactor: 0.8, // scales pointer dy influence on pattern offset
  patternLayers: 5, // number of layered arcs/lines per wedge
  patternMode: 'starburst',
  patternModes: ['starburst', 'bandsLines', 'geoRings', 'petals'],
});

// Curated color palettes
const CuratedPalettes = [
  { name: 'Neon Night', colors: [
    'hsl(200 85% 60%)', 'hsl(260 90% 66%)', 'hsl(320 80% 60%)', 'hsl(180 80% 55%)'
  ]},
  { name: 'Sunset Candy', colors: [
    'hsl(12 85% 60%)', 'hsl(340 72% 62%)', 'hsl(280 70% 62%)', 'hsl(45 90% 64%)'
  ]},
  { name: 'Aurora', colors: [
    'hsl(160 70% 55%)', 'hsl(200 70% 60%)', 'hsl(90 60% 58%)', 'hsl(48 80% 60%)'
  ]},
  { name: 'Oceanic', colors: [
    'hsl(197 92% 54%)', 'hsl(210 70% 60%)', 'hsl(175 65% 55%)', 'hsl(230 60% 66%)'
  ]},
  { name: 'Magma', colors: [
    'hsl(10 85% 55%)', 'hsl(20 80% 58%)', 'hsl(340 70% 60%)', 'hsl(50 90% 60%)'
  ]},
  { name: 'Nord', colors: [
    'hsl(210 34% 63%)', 'hsl(222 27% 74%)', 'hsl(198 33% 52%)', 'hsl(193 54% 33%)'
  ]}
];

function randomCuratedPalette() {
  const i = randInt(0, CuratedPalettes.length - 1);
  return CuratedPalettes[i];
}

// ----- Utility helpers -----
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const lerp = (a, b, t) => a + (b - a) * t;
const TAU = Math.PI * 2;

function rand(min = 0, max = 1) { return Math.random() * (max - min) + min; }
function randInt(min, max) { return Math.floor(rand(min, max + 1)); }
function randomPalette() {
  // Generate 3-5 HSL colors with harmonious hues
  const count = randInt(3, 5);
  const baseHue = rand(0, 360);
  const colors = Array.from({ length: count }, (_, i) => {
    const hue = (baseHue + i * rand(18, 46)) % 360;
    const sat = rand(55, 85);
    const light = rand(40, 70);
    return `hsl(${hue.toFixed(1)} ${sat.toFixed(1)}% ${light.toFixed(1)}%)`;
  });
  return { name: 'Procedural', colors };
}

// Soft pseudo-noise from trig combos
function softNoise(x, y, t) {
  return (
    Math.sin(x * 1.7 + t * 0.6) * 0.6 +
    Math.cos(y * 1.3 - t * 0.4) * 0.4 +
    Math.sin((x + y) * 0.5 + t * 0.9) * 0.3
  );
}

// ----- KaleidoscopeRenderer -----
class KaleidoscopeRenderer {
  constructor(canvas, config) {
    this.canvas = canvas;
    this.ctx = canvas.getContext('2d', { alpha: true });
    this.config = { ...config };
    this.dpr = Math.max(1, window.devicePixelRatio || 1);
    this.center = { x: 0, y: 0 };
    this.radius = 0;

    this.rotation = 0; // radians
    this.phase = 0; // pattern phase
    const initial = randomCuratedPalette();
    this.palette = initial.colors;
    this.paletteName = initial.name;
    this.bandsDots = []; // precomputed static dots for bands+lines

    this.resize();
    // Initialize static dots based on current geometry
    this._regenBandsDots(this.radius, TAU / this.config.segments);
  }

  setSegments(n) {
    const clamped = clamp(n, this.config.minSegments, this.config.maxSegments);
    this.config.segments = clamped;
    // Regenerate static dots when wedge angle changes
    this._regenBandsDots(this.radius, TAU / this.config.segments);
  }

  randomize() {
    // Prefer curated palettes most of the time
    const useCurated = Math.random() < 0.7;
    const pal = useCurated ? randomCuratedPalette() : randomPalette();
    this.palette = pal.colors;
    this.paletteName = pal.name;
    // Small phase jump to visibly change pattern dynamics
    this.phase = rand(0, TAU);
    // Occasionally switch pattern mode too
    if (Math.random() < 0.4) {
      const modes = this.config.patternModes || [this.config.patternMode];
      const next = modes[randInt(0, modes.length - 1)];
      this.setPatternMode(next);
    }
    // Regenerate static dots to match new palette (colors only)
    this._regenBandsDots(this.radius, TAU / this.config.segments);
  }

  setPaused(p) { this.config.paused = !!p; }

  setPatternMode(mode) {
    if (!mode) return;
    if ((this.config.patternModes || []).includes(mode)) {
      this.config.patternMode = mode;
    }
  }

  setPalette(paletteObj) {
    if (!paletteObj) return;
    this.palette = paletteObj.colors;
    this.paletteName = paletteObj.name;
    this._regenBandsDots(this.radius, TAU / this.config.segments);
  }

  resize() {
    const cssWidth = window.innerWidth;
    const cssHeight = window.innerHeight;
    const dpr = Math.max(1, window.devicePixelRatio || 1);
    this.dpr = dpr;

    this.canvas.style.width = cssWidth + 'px';
    this.canvas.style.height = cssHeight + 'px';
    this.canvas.width = Math.floor(cssWidth * dpr);
    this.canvas.height = Math.floor(cssHeight * dpr);

    // Reset transform and scale by dpr so drawing uses CSS pixels
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    this.center.x = cssWidth / 2;
    this.center.y = cssHeight / 2;
    this.radius = Math.hypot(cssWidth, cssHeight) * 0.6; // slightly oversized

    // Regenerate static dots using new radius and current segments
    this._regenBandsDots(this.radius, TAU / this.config.segments);
  }

  update(dt, input) {
    // dt: seconds; input: { rotInfluence, offsetInfluence }
    const base = this.config.baseRotationSpeed;
    const rotInfluence = (input?.rotInfluence || 0) * this.config.pointerRotationFactor;
    const speed = base + rotInfluence; // radians/sec
    this.rotation += speed * dt;

    const offInfluence = (input?.offsetInfluence || 0) * this.config.pointerOffsetFactor;
    this.phase += (0.6 + Math.abs(offInfluence)) * dt; // phase animates continuously
  }

  draw() {
    const { ctx, center, radius } = this;
    const segs = this.config.segments;
    const theta = TAU / segs;

    // Clear
    ctx.clearRect(0, 0, this.canvas.width / this.dpr, this.canvas.height / this.dpr);

    // Translate to center for wedge drawing
    ctx.save();
    ctx.translate(center.x, center.y);

    // Per-segment drawing
    for (let i = 0; i < segs; i++) {
      ctx.save();
      ctx.rotate(this.rotation + i * theta);
      if (i % 2 === 1) ctx.scale(-1, 1); // mirror alternating segments

      // Clip to wedge
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.arc(0, 0, radius, -theta / 2, theta / 2, false);
      ctx.closePath();
      ctx.clip();

      // Draw the procedural pattern inside the wedge
      this.drawPatternWedge(ctx, radius, theta);

      ctx.restore();
    }

    ctx.restore();
  }

  drawPatternWedge(ctx, radius, theta) {
    const mode = this.config.patternMode || 'bandsLines';
    if (mode === 'bandsLines') {
      this._drawBandsLines(ctx, radius, theta);
    } else if (mode === 'starburst') {
      this._drawStarburst(ctx, radius, theta);
    } else if (mode === 'geoRings') {
      this._drawGeoRings(ctx, radius, theta);
    } else if (mode === 'petals') {
      this._drawPetals(ctx, radius, theta);
    } else {
      this._drawBandsLines(ctx, radius, theta);
    }
  }

  // Precompute static dots for bands+lines mode
  _regenBandsDots(radius, theta) {
    const count = 24;
    this.bandsDots = Array.from({ length: count }, (_, i) => {
      const ang = lerp(-theta / 2, theta / 2, Math.random());
      const rad = lerp(radius * 0.04, radius * 0.92, Math.random());
      const size = 0.9 + Math.random() * 2.2;
      const colorIndex = i % this.palette.length;
      return { ang, rad, size, colorIndex };
    });
  }

  _drawBandsLines(ctx, radius, theta) {
    const layers = this.config.patternLayers;
    const t = this.phase;
    // Radial bands
    for (let l = 0; l < layers; l++) {
      const r0 = (l / layers) * radius;
      const r1 = ((l + 1) / layers) * radius;
      const color = this.palette[l % this.palette.length];
      const grad = ctx.createRadialGradient(0, 0, r0, 0, 0, r1);
      grad.addColorStop(0, color);
      grad.addColorStop(1, 'transparent');
      ctx.fillStyle = grad;
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.arc(0, 0, r1, -theta / 2, theta / 2);
      ctx.closePath();
      ctx.fill();
    }
    // Flowing lines
    const lines = 28;
    ctx.lineWidth = 1.2;
    for (let k = 0; k < lines; k++) {
      const f = k / lines;
      const color = this.palette[(k + 1) % this.palette.length];
      ctx.strokeStyle = color;
      const rStart = lerp(radius * 0.05, radius * 0.9, f);
      const noisey = softNoise(f * 5.0, rStart * 0.01, t);
      const bend = noisey * (theta * 0.35);
      ctx.beginPath();
      const a0 = -theta / 2 + bend * 0.4;
      const a1 = theta / 2 - bend * 0.6;
      for (let s = 0; s <= 20; s++) {
        const sLerp = s / 20;
        const ang = lerp(a0, a1, sLerp);
        const rad = lerp(rStart, rStart + radius * 0.08 * Math.abs(noisey), sLerp);
        ctx.lineTo(Math.cos(ang) * rad, Math.sin(ang) * rad);
      }
      ctx.stroke();
    }
    // Static spark dots (precomputed)
    ctx.globalAlpha = 0.85;
    const dots = this.bandsDots;
    for (let i = 0; i < dots.length; i++) {
      const d = dots[i];
      ctx.fillStyle = this.palette[d.colorIndex % this.palette.length];
      ctx.beginPath();
      ctx.arc(Math.cos(d.ang) * d.rad, Math.sin(d.ang) * d.rad, d.size, 0, TAU);
      ctx.fill();
    }
    ctx.globalAlpha = 1;
  }

  _drawStarburst(ctx, radius, theta) {
    const t = this.phase;
    // Background soft radial gradient
    const grad = ctx.createRadialGradient(0, 0, 0, 0, 0, radius);
    grad.addColorStop(0, 'rgba(255,255,255,0.04)');
    grad.addColorStop(1, 'transparent');
    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.arc(0, 0, radius, -theta / 2, theta / 2);
    ctx.closePath();
    ctx.fill();

    // Radial rays
    const rays = 36;
    for (let i = 0; i < rays; i++) {
      const f = i / rays;
      const hueColor = this.palette[i % this.palette.length];
      ctx.strokeStyle = hueColor;
      ctx.lineWidth = lerp(0.6, 2.2, Math.abs(Math.sin(t * 0.8 + i)));
      const bend = softNoise(f * 3.0, t, t) * (theta * 0.2);
      const a = lerp(-theta / 2, theta / 2, f) + bend;
      ctx.beginPath();
      ctx.moveTo(Math.cos(a) * (radius * 0.08), Math.sin(a) * (radius * 0.08));
      ctx.lineTo(Math.cos(a) * radius, Math.sin(a) * radius);
      ctx.stroke();
    }

    // Sparkles at ray tips
    for (let j = 0; j < 24; j++) {
      const a = lerp(-theta / 2, theta / 2, Math.random());
      const r = lerp(radius * 0.7, radius, Math.random());
      const size = 0.6 + Math.random() * 2.0;
      ctx.fillStyle = this.palette[j % this.palette.length];
      ctx.beginPath();
      ctx.arc(Math.cos(a) * r, Math.sin(a) * r, size, 0, TAU);
      ctx.fill();
    }
  }

  _drawGeoRings(ctx, radius, theta) {
    const t = this.phase;
    const rings = 7;
    for (let r = 1; r <= rings; r++) {
      const rr = lerp(radius * 0.22, radius * 0.96, r / rings);
      const sides = 6 + (r % 5); // 6..10 for bolder geometry
      const points = [];
      for (let s = 0; s < sides; s++) {
        const f = s / sides;
        const ang = lerp(-theta / 2, theta / 2, f) + softNoise(f * 1.6, rr * 0.015, t) * (theta * 0.12);
        const wobble = 1 + softNoise(f * 3.0, t * 0.5, t) * 0.08;
        points.push({ x: Math.cos(ang) * rr * wobble, y: Math.sin(ang) * rr * wobble });
      }

      // Fill ring with subtle alpha
      ctx.beginPath();
      points.forEach((p, idx) => { if (idx === 0) ctx.moveTo(p.x, p.y); else ctx.lineTo(p.x, p.y); });
      ctx.closePath();
      ctx.globalAlpha = 0.14;
      ctx.fillStyle = this.palette[(r + 1) % this.palette.length];
      ctx.fill();
      ctx.globalAlpha = 1;

      // Stroke outline thicker
      ctx.strokeStyle = this.palette[r % this.palette.length];
      ctx.lineWidth = 1.8;
      ctx.stroke();

      // Add radial spokes for structure
      ctx.strokeStyle = this.palette[(r + 2) % this.palette.length];
      ctx.lineWidth = 1.1;
      for (let i = 0; i < points.length; i += 2) {
        const p = points[i];
        ctx.beginPath();
        ctx.moveTo(0, 0);
        ctx.lineTo(p.x, p.y);
        ctx.stroke();
      }
    }
  }

  _drawNoiseFlow(ctx, radius, theta) {
    const t = this.phase;
    const curves = 28; // fewer curves for calmer look
    ctx.lineWidth = 1.1;
    for (let c = 0; c < curves; c++) {
      const color = this.palette[c % this.palette.length];
      ctx.strokeStyle = color;
      const a0 = lerp(-theta / 2, theta / 2, Math.random());
      const r0 = lerp(radius * 0.08, radius * 0.88, Math.random());
      ctx.beginPath();
      for (let s = 0; s <= 24; s++) {
        const u = s / 24;
        // slower temporal influence and reduced angular noise amplitude
        const ang = lerp(a0 - theta * 0.2, a0 + theta * 0.2, u) + softNoise(u * 2.4, t * 0.3 + c * 0.2, t) * (theta * 0.18);
        const rad = lerp(r0, r0 + radius * 0.12, u);
        ctx.lineTo(Math.cos(ang) * rad, Math.sin(ang) * rad);
      }
      ctx.stroke();
    }
  }

  _drawPetals(ctx, radius, theta) {
    const t = this.phase;
    const layers = 6;
    const steps = 42;
    for (let l = 0; l < layers; l++) {
      const f = l / (layers - 1);
      const baseR = lerp(radius * 0.18, radius * 0.95, f);
      const freq = 3 + (l % 3); // petal count per wedge
      const amp = baseR * 0.06; // gentle modulation

      // Draw smooth petal curve along wedge
      ctx.beginPath();
      for (let s = 0; s <= steps; s++) {
        const u = s / steps;
        const ang = lerp(-theta / 2, theta / 2, u);
        const r = baseR + Math.sin(ang * freq + t * 0.35 + l * 0.4) * amp;
        const x = Math.cos(ang) * r;
        const y = Math.sin(ang) * r;
        if (s === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = this.palette[l % this.palette.length];
      ctx.lineWidth = 1.4;
      ctx.stroke();

      // Subtle fill under curve
      ctx.globalAlpha = 0.10;
      ctx.fillStyle = this.palette[(l + 1) % this.palette.length];
      ctx.fill();
      ctx.globalAlpha = 1;
    }

    // Center bloom
    const bloom = ctx.createRadialGradient(0, 0, 0, 0, 0, radius * 0.22);
    bloom.addColorStop(0, 'rgba(255,255,255,0.05)');
    bloom.addColorStop(1, 'transparent');
    ctx.fillStyle = bloom;
    ctx.beginPath();
    ctx.moveTo(0, 0);
    ctx.arc(0, 0, radius * 0.22, -theta / 2, theta / 2);
    ctx.closePath();
    ctx.fill();
  }
}

// ----- InputController -----
class InputController {
  constructor(canvas) {
    this.canvas = canvas;
    this.pointer = { x: 0, y: 0, dx: 0, dy: 0, down: false };
    this.bounds = { w: window.innerWidth, h: window.innerHeight };

    this._onPointerMove = this._onPointerMove.bind(this);
    this._onPointerDown = this._onPointerDown.bind(this);
    this._onPointerUp = this._onPointerUp.bind(this);

    canvas.addEventListener('pointermove', this._onPointerMove, { passive: true });
    canvas.addEventListener('pointerdown', this._onPointerDown);
    window.addEventListener('pointerup', this._onPointerUp);
    window.addEventListener('resize', () => {
      this.bounds.w = window.innerWidth;
      this.bounds.h = window.innerHeight;
    });
  }

  _onPointerMove(e) {
    const rect = this.canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    this.pointer.dx = x - this.pointer.x;
    this.pointer.dy = y - this.pointer.y;
    this.pointer.x = x;
    this.pointer.y = y;
  }
  _onPointerDown() { this.pointer.down = true; }
  _onPointerUp() { this.pointer.down = false; }

  // Influence values for rotation and pattern offset
  getInfluence() {
    const { dx, dy } = this.pointer;
    const rotInfluence = clamp(dx / Math.max(120, this.bounds.w), -1, 1);
    const offsetInfluence = clamp(dy / Math.max(120, this.bounds.h), -1, 1);
    // decay dx/dy slightly to avoid continuous influence when stationary
    this.pointer.dx *= 0.92;
    this.pointer.dy *= 0.92;
    return { rotInfluence, offsetInfluence };
  }
}

// ----- UIController -----
class UIController {
  constructor(app) {
    this.app = app;
    this.el = {
      segments: document.getElementById('segments-count'),
      status: document.getElementById('run-status'),
      pattern: document.getElementById('pattern-name'),
      palette: document.getElementById('palette-name'),
      btnInc: document.getElementById('btn-inc'),
      btnDec: document.getElementById('btn-dec'),
      btnRandom: document.getElementById('btn-random'),
      btnToggle: document.getElementById('btn-toggle'),
      btnPattern: document.getElementById('btn-pattern'),
    };
    this._bind();
    this.updateStatus();
  }

  _bind() {
    this.el.btnInc.addEventListener('click', () => this.app.changeSegments(1));
    this.el.btnDec.addEventListener('click', () => this.app.changeSegments(-1));
    this.el.btnRandom.addEventListener('click', () => this.app.randomize());
    this.el.btnToggle.addEventListener('click', () => this.app.togglePause());
    this.el.btnPattern.addEventListener('click', () => this.app.cyclePattern());
  }

  updateStatus() {
    this.el.segments.textContent = String(this.app.renderer.config.segments);
    const running = !this.app.renderer.config.paused;
    this.el.status.textContent = running ? 'Running' : 'Paused';
    this.el.btnToggle.textContent = running ? 'Pause' : 'Resume';
    this.el.pattern.textContent = this.app.renderer.config.patternMode;
    this.el.palette.textContent = this.app.renderer.paletteName || '—';
  }
}

// ----- App -----
class App {
  constructor() {
    this.canvas = document.getElementById('kaleidoscope');
    this.renderer = new KaleidoscopeRenderer(this.canvas, Defaults);
    this.input = new InputController(this.canvas);
    this.ui = new UIController(this);

    this._lastTime = performance.now();
    this._loop = this._loop.bind(this);

    this._bindKeyboard();
    window.addEventListener('resize', () => {
      this.renderer.resize();
    });

    requestAnimationFrame(this._loop);
  }

  _bindKeyboard() {
    window.addEventListener('keydown', (e) => {
      if (e.key === '[') {
        e.preventDefault();
        this.changeSegments(-1);
      } else if (e.key === ']') {
        e.preventDefault();
        this.changeSegments(1);
      } else if (e.key === 'r' || e.key === 'R') {
        e.preventDefault();
        this.randomize();
      } else if (e.key === 'p' || e.key === 'P') {
        e.preventDefault();
        this.cyclePattern();
      } else if (e.key === 'c' || e.key === 'C') {
        e.preventDefault();
        this.cyclePalette();
      } else if (e.key === ' ') {
        e.preventDefault();
        this.togglePause();
      }
    });
  }

  changeSegments(delta) {
    const cur = this.renderer.config.segments;
    this.renderer.setSegments(cur + delta);
    this.ui.updateStatus();
  }

  randomize() {
    this.renderer.randomize();
    this.ui.updateStatus();
  }

  togglePause() {
    const paused = !this.renderer.config.paused;
    this.renderer.setPaused(paused);
    this.ui.updateStatus();
  }

  cyclePattern() {
    const modes = this.renderer.config.patternModes;
    const cur = this.renderer.config.patternMode;
    const idx = modes.indexOf(cur);
    const next = modes[(idx + 1) % modes.length];
    this.renderer.setPatternMode(next);
    this.ui.updateStatus();
  }

  cyclePalette() {
    const currentName = this.renderer.paletteName;
    const idx = CuratedPalettes.findIndex(p => p.name === currentName);
    const next = CuratedPalettes[(idx + 1) % CuratedPalettes.length];
    this.renderer.setPalette(next);
    this.ui.updateStatus();
  }

  _loop(now) {
    const dt = Math.min(0.05, (now - this._lastTime) / 1000); // clamp large steps
    this._lastTime = now;

    if (!this.renderer.config.paused) {
      const influence = this.input.getInfluence();
      this.renderer.update(dt, influence);
      this.renderer.draw();
    }

    requestAnimationFrame(this._loop);
  }
}

// Initialize top-level App instance on DOM ready
window.addEventListener('DOMContentLoaded', () => {
  // Single app instance without exposing globals
  new App();
});
