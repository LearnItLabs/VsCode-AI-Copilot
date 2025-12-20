# Kaleidoscope Site Prompt (Ready to Copy)

Build a small, modern interactive kaleidoscope website using plain HTML + modern CSS + vanilla JavaScript. No frameworks, no libraries, no bundlers, and no inline styles/scripts. The site must run by opening index.html directly.

## Files
- index.html: semantic structure only
- styles.css: all styling (system fonts, dark theme)
- app.js: all JavaScript (ES6+, classes, no globals; single top-level App)

## Core Features
- Rendering: full-viewport <canvas>, high-DPI handling via devicePixelRatio, responsive resize. Kaleidoscope symmetry by dividing the circle into N segments (configurable: min 6, max 24; default 12), mirroring alternating segments. Smooth animation via requestAnimationFrame.
- Patterns: procedural (math-based; no images). Include multiple modes and a cycle:
  - bandsLines (layered gradients + flowing lines; dots are precomputed/static)
  - starburst (rays with gentle modulation)
  - geoRings (bold polygonal rings with spokes)
  - petals (layered petal-like curves + soft center bloom)
  Start mode: starburst. Provide a clean API to add more modes later.
- Palettes: curated named sets (e.g., Neon Night, Sunset Candy, Aurora, Oceanic, Magma, Nord) plus a “Procedural” generator. Show the active palette name in the UI. Randomize prefers curated palettes most of the time. Cycling palettes updates colors and any precomputed elements.
- Interactivity: mouse/touch movement influences rotation speed and/or pattern offset. Keyboard shortcuts:
  - [ and ]: change segment count
  - R: randomize palette/pattern parameters
  - Space: pause/resume
  - P: cycle pattern modes
  - C: cycle curated palettes
- UI overlay: unobtrusive modern dark panel (bottom-left), system fonts only, subtle blur/alpha, focus and hover states. Show segment count, running/paused status, current pattern, and palette name. Provide buttons: - / + segments, Randomize, Pattern (cycle), Pause/Resume.

## JavaScript Architecture (single file, no bundlers)
- Modules/classes within app.js:
  - Config/defaults (bounds for segments, rotation, layers, pattern modes)
  - KaleidoscopeRenderer (canvas setup, high-DPI, symmetry, draw patterns, precomputed elements where needed)
  - InputController (pointer + keyboard)
  - UIController (DOM controls + status)
  - App (init, resize, loop; single instance)
- Keep functions small and named clearly; use ES6 features; avoid global variables.

## CSS Architecture
- Consistent naming (BEM-like), flexbox/grid layout for the overlay.
- Dark theme variables, system fonts, focus styles, hover states.
- Minimal canvas styling; overlay with subtle blur/alpha and accessible contrast.

## Implementation Details
- Precompute static dots for the bandsLines mode (regenerate on resize or segment change).
- devicePixelRatio-aware transforms so drawing uses CSS pixels.
- Clamp dt in the loop to handle tab switching.

## Deliverables
- Provide complete working code for index.html, styles.css, and app.js.
- Ensure it runs offline by opening index.html.
