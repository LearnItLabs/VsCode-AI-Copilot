## Prompt 2 — Conceptual, Goal-Oriented

> “Refactor this monolithic HTML page to improve separation of concerns.  
> Goal: move all CSS into an external stylesheet and all JavaScript into an external script file, while keeping behavior and appearance unchanged.”

---

###  What Copilot will likely do:
- Treat this as a refactoring task, not just a file split.
- Decide file names itself (e.g., `style.css`, `main.css`, `script.js`, `main.js`)
- Preserve all behavior exactly as written
- Recreate inline event handlers as proper JS functions
- Possibly reorganize JS into cleaner functions or modules
- Possibly reorganize CSS for clarity
- Ensure the UI looks identical
- Avoid breaking subtle interactions

---

### How Copilot interprets it:
- “The user wants a cleaner architecture, not just a file split.”
- More reasoning, more restructuring, more attention to behavior parity.

---

### Result:
A thoughtful refactor, not just extraction.
