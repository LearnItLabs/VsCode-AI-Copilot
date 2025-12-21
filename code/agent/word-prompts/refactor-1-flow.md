**Prompt 1 — Highly Specific, Procedural**  
“Split this HTML page into `index.html`, `styles.css`, and `app.js`. Remove inline CSS/JS and inline event handlers.”

---

###  What Copilot will likely do:
- Treat this as a direct, mechanical transformation.
- Create exactly three files with those exact names.
- Move CSS → `styles.css`
- Move JS → `app.js`
- Strip inline event handlers (`onclick=`, etc.)
- Remove inline `<style>` and `<script>` blocks
- Update the HTML to reference the new files

---

### How Copilot interprets it:
- “I know exactly what the user wants. Execute the steps literally.”
- Minimal reasoning about architecture or behavior.
- No need to preserve subtle interactions unless they break.

---

###  Result:
A literal split of the page.
