# Built‑In Copilot Chat Variables

These variables pull real context from your editor into the chat.  
You don’t define them — you just use them.

| Chat Variable   | What It References                           | Typical Use Case                        | Example Prompt                                      |
|-----------------|-----------------------------------------------|------------------------------------------|------------------------------------------------------|
| `#file`         | Entire contents of the active editor file     | Ask about or transform the whole file    | Summarize `#file` in plain English.                 |
| `#selection`    | The currently highlighted text                | Refactor or explain a specific block     | Rewrite `#selection` using modern JS.               |
| `#code`         | Code from the active file (code‑aware)        | Code‑specific analysis or improvements   | Add JSDoc comments to `#code`.                      |
| `#editor`       | Full editor context (file, language, cursor)  | Tasks depending on editor state          | Suggest improvements based on `#editor`.            |
| `#terminal`     | Most recent terminal output                   | Debugging CLI or build errors            | Explain the error in `#terminal`.                   |
| `#problems`     | Current Problems panel (errors, warnings)     | Fixing issues across the workspace       | Help me resolve the issues in `#problems`.          |
| `#gitChanges`   | Diff of uncommitted changes                   | Reviewing or summarizing changes         | Write a commit message for `#gitChanges`.           |
| `#repo`         | Entire repository context                     | Repo‑wide tasks or architecture analysis | Generate documentation for